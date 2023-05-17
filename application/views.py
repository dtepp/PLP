from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file,jsonify,session
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like, Follower
import requests
import io
import pandas as pd
from .Database import db
from .DataRelated.Dataprepocessing import getEntity
#from .CNNModel.OverallSentiment import predict_review
import json
from .CNNModel.T5 import translation


views = Blueprint("views", __name__)



@views.route("/")
@views.route("/home")
@login_required
def home():
    # Get the IDs of users that the current user is following
    following_ids = []
    for follower in current_user.following:
        following_ids.append(follower.user_id)
    # Get the posts created by users that the current user is following
    following_posts = Post.query.filter(Post.author.in_(following_ids)).all()
    # Get the current user's posts
    user_posts = current_user.posts
    # Combine the two lists of posts
    posts = following_posts + user_posts
    return render_template("home.html", user=current_user, posts=posts)


@login_required
@views.route("/savepost", methods=['POST'])
def save_post():
    if request.method == "POST":
        # Get text from request form
        text = request.form.get('text')
    
            # Create new post object with text and current user's ID
        post = Post(text=text, author=current_user.id)
            # Add post to database session
        db.session.add(post)
            # Commit changes to the database
        db.session.commit()
            # Flash success message
        flash("Evaluation created!", category='success')
            # Redirect to home page
        return redirect(url_for('views.home'))



@login_required
@views.route("/create-post", methods=['GET', 'POST'])
def create_post():
    # Check if request method is POST
    if request.method == "POST":
        # Get text from request form
        text = request.form.get('text')
        # Get uploaded file
        file = request.files.get('file')
       
        # Check if text is empty
        if  text =="":
            flash("Evaluation description cannot be empty", category="error")
        elif  file.filename=="":
            flash("Please select a file to upload.", category="error")
        else:
            # Read file content
            file_content = file.read()
            file_extension = file.filename.rsplit('.', 1)[1].lower()
           
            if file_extension in {'xls', 'xlsx'}:
                # Read Excel data using pandas
                df = pd.read_excel(io.BytesIO(file_content),header=0)

            elif file_extension == 'csv':
                # Read CSV data using pandas
                # List of possible encoding formats to try
                encoding_formats = ['utf-8', 'latin1', 'utf-16', 'utf-32', 'cp1252', 'iso-8859-1']

                # Iterate through each encoding format and try reading the CSV file
                for encoding in encoding_formats:
                    try:
                        df = pd.read_csv(io.BytesIO(file_content), encoding=encoding, header=0)
                        break
                    except UnicodeDecodeError:
                        continue
            # Convert DataFrame to dictionary
            
            data = df.values.tolist()
            session['data'] = data
            return jsonify(data)

    # Render the create_post template
    return render_template("create_post.html", user=current_user, User=User)



@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    # Get post with specified id
    post = Post.query.filter_by(id=id).first()

    # Check if post exists
    if not post:
        flash("Evaluation does not exist", category='error')
    else:
        # Delete post from the database
        db.session.delete(post)
        # Commit changes to the database
        db.session.commit()
        flash('Evaluation deleted', category="success")

    # Redirect to home page
    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def post(username):
    # Get the user with the specified username
    user = User.query.filter_by(username=username).first()
    # Check if the user exists
    if not user:
        flash("No with that username exist", category="error")
        redirect(url_for('views.home'))
    # Get all posts by the user
    posts = user.posts

    user_id = user.id

    # Check if the current user is following the user
    following = Follower.query.filter_by(
        user_id=user.id, follower_id=current_user.id).first()

    # Render the posts template and pass the current user, posts, username, User, following, and user_id
    return render_template("posts.html", user=current_user, posts=posts, username=username, User=User, following=following, user_id=user_id)


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    # Get text from request form
    text = request.form.get('text')

    # Check if text is empty
    if not text:
        flash("Comment can not be empty", category="error")
    else:
        # Get the post with the specified id
        post = Post.query.filter_by(id=post_id).first()
        # Check if post exists
        if post:
            # Create new comment object with text, current user's ID, and post_id
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            # Add comment to database session
            db.session.add(comment)
            # Commit changes to the database
            db.session.commit()
        else:
            flash("Evaluation does not exist", category="error")

    # Redirect to home page
    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    # Get the comment with the specified id
    comment = Comment.query.filter_by(id=comment_id).first()

    # Check if the comment exists
    if not comment:
        flash('Comment does not exist.', category='error')
    # Check if the current user is the author of the comment or the post
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        # Delete the comment from the database
        db.session.delete(comment)
        # Commit changes to the database
        db.session.commit()

    # Redirect to the home page
    return redirect(url_for('views.home'))


@views.route("/like-post/<post_id>", methods=["GET"])
@login_required
def like(post_id):
    # Get the post with the specified id
    post = Post.query.filter_by(id=post_id).first()
    # Get the like by the current user on the post
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    # Check if the post exists
    if not post:
        flash('Evaluation does not exist', category='error')
    # Check if the current user has already liked the post
    elif like:
        # Unlike the post
        db.session.delete(like)
        db.session.commit()
    else:
        # Create a new like
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # Redirect to the home page
    return redirect(url_for('views.home'))



@views.route("/preprocess", methods=['POST'])
def preprocess():
    # Process the uploaded file data and return the processed data
    # You can update this logic based on your specific preprocessing requirements

    # Example: Process the data by converting all text to uppercase
    data = session.get('data')
    result=pd.DataFrame()
    for item in data:

        text=" ".join(item)
        processtext= getEntity(text)
        result=pd.concat([result,processtext],ignore_index=True)

    # Return the processed data as JSON response
    return jsonify(result.to_dict(orient='records'))


@views.route("/sentiment", methods=['POST'])
def sentiment():
    # Process the uploaded file data and return the processed data
    # You can update this logic based on your specific preprocessing requirements
    preprocessed = json.loads(request.form.get("preprocess"))
    # Example: Process the data by converting all text to uppercase
  
    
   
    overallNum=0
    overallPos=0
    FoodNum=0
    FoodPos=0
    PriceNum=0
    PricePos=0
    environmentNum=0
    environmentPos=0
    serviceNum=0
    servicePos=0
    
    data=session.get('data')
    overallNum=len(data)
    for text in data:
        
            result=predict_review(text)
            
            if result:
                overallPos=overallPos+1
            else:
                continue 
  

    for dict in preprocessed:
        result=predict_review(dict["sentence"])
        for domain in  dict["domain"]:
            if "food" in domain:
                FoodNum=FoodNum+1
                if result:
                        FoodPos=FoodPos+1
                else:
                        continue 
            elif "price" in domain:
                PriceNum=PriceNum+1
                if result:
                        PricePos=PricePos+1
                else:
                        continue 
            elif "environment" in domain:
                environmentNum=environmentNum+1
                if result:
                        environmentPos=environmentPos+1
                else:
                        continue 
            elif "service" in domain:
                serviceNum=serviceNum+1
                if result:
                        servicePos=servicePos+1
                else:
                        continue 
            else:
                continue
        
    Summary="There are "+str(overallNum)+" customer reviews, "+str(overallPos)+" of them is positive."
    Food="There are "+str(FoodNum)+" comment on food, "+str(FoodPos)+" of them is positive."
    Price="There are "+str(PriceNum)+" comment on price, "+str(PricePos)+" of them is positive."
    environment="There are "+str(environmentNum)+" comment on environment, "+str(environmentPos)+" of them is positive."
    service="There are "+str(serviceNum)+" comment on service, "+str(servicePos)+" of them is positive."
    # Return the processed data as JSON response
    resultlist=[Summary,Food,Price,environment,service]
    return jsonify(resultlist)

