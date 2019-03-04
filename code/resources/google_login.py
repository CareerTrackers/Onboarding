from flask import g, request, url_for, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from oa import google
from models.user import UserModel

import time

class GoogleLogin(Resource):
  @classmethod
  def get(cls):
    return google.authorize(url_for("google.authorize", _external=True))


class GoogleAuthorize(Resource):
  @classmethod
  def get(cls):
    resp = google.authorized_response()
    if resp is None or resp.get("access_token") is None:
      error_response = {
        "error": request.args['error'],
        "error_description": request.args["error_description"]
      }
      return error_response

    g.access_token = resp['access_token']
    google_user = google.get('userinfo')
    google_email = google_user.data['email']

    #region
    # user = UserModel.find_by_email(google_email)
    # if not user:
    #   newUser = UserModel(
    #     google_email,
    #     google_user.data['given_name'],
    #     google_user.data['family_name']
    #   )
    #   newUser.save_to_db()
    #endregion

    user = UserModel.find_by_email(google_email)
    if not user:
      newUser = UserModel(
        google_email,
        google_user.data['given_name'],
        google_user.data['family_name']
      )
      newUser.save_to_db()
      time.sleep(5.5)
      #TODO: implement "try again" code for the above, perhaps using Tenacity

    access_token = create_access_token(identity = user.id, fresh = True)
    refresh_token = create_refresh_token(user.id)

    return {
      "access_token": access_token, 
      "refresh_token": refresh_token,
      "user_id": user.id,
      "google_username": google_user.data['email'],
      "google_userid": google_user.data['id']
      }, 200