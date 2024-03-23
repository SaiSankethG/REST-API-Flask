from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

video_args = reqparse.RequestParser()
video_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_args.add_argument("likes", type=int, help="Views of the video", required=True)
video_args.add_argument("views", type=int, help="Likes on the video", required=True)

video_pargs = reqparse.RequestParser()
video_pargs.add_argument("name", type=str, help="name of the video")
video_pargs.add_argument("likes", type=int, help="views of the video")
video_pargs.add_argument("views", type=int, help="likes of the video")

resource_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'likes':fields.Integer,
    'views':fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found...")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video already exists...")
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_pargs.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "video not exists!! to update")
        if args['name']:
            result.name = args['name']
        if args['likes']:
            result.likes = args['likes']
        if args['views']:
            result.views = args['views']
        db.session.commit()
        
        return result
                
    def delete(self, video_id):
        abort_if_video_id_not_found(video_id)
        del videos[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
