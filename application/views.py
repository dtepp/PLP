from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file,jsonify,session
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
import requests
import io
import pandas as pd
from .Database import db
from .SentimentAnalysis import ReviewAnalysis

import json


views = Blueprint("views", __name__)



@views.route("/")
@views.route("/home")
@login_required
def home():

  

    # Get the current user's posts
    user_posts = current_user.posts
    # Combine the two lists of posts
    posts = user_posts
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/new")
@login_required
def new():
    return render_template("new.html", user=current_user)


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

            data = df.values.tolist()
            inputtext=df.iloc[:, 0].values.tolist()
            (TranslateResult,OverallResult,Newdomainsentiment,df_sorted)=ReviewAnalysis(inputtext)
           
            df_sorted_json = df_sorted.to_dict(orient='records')
            return jsonify({
                            'TranslateResult': TranslateResult,
                            'OverallResult': OverallResult,
                            'Newdomainsentiment': Newdomainsentiment,
                            'df_sorted': df_sorted_json
                        })

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

   
    # Render the posts template and pass the current user, posts, username, User, following, and user_id
    return render_template("posts.html", user=current_user, posts=posts, username=username, User=User, following=0, user_id=user_id)


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


