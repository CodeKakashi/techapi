from app.authLogin.auth import EditProfile, Login, AdminSignUp
from app.authLogin.user import CreateUser, ApprovalList, ApproveAdmin
from . import auth_api

auth_api.add_resource(Login, "/login")
auth_api.add_resource(AdminSignUp, "/register")
auth_api.add_resource(EditProfile, "/edit/profile")
auth_api.add_resource(ApprovalList, "/get/approvalList/<approvalType>")
auth_api.add_resource(ApproveAdmin, "/approveAdmin")
# Sample Commit


auth_api.add_resource(CreateUser, "/create/user/<uid>")