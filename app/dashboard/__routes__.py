from app.dashboard.complaint import ComplaintForm
from app.dashboard.contactus import ContactUs, Quotation
from app.dashboard.dashboard import Dashboard, ClientDetails, DeleteClient
from app.dashboard.ping import Ping
from app.dashboard.planDetails import CollectionList, UpdateCollectionList, PlanDetails, PlanUpdate
from app.dashboard.statistics import AdminCensus, ClientSchedule
from . import dashboard_api

dashboard_api.add_resource(Dashboard, "/get/dashboard")
dashboard_api.add_resource(ComplaintForm, "/complaintForm")
dashboard_api.add_resource(ContactUs, "/get/contact")
dashboard_api.add_resource(PlanDetails, "/get/plan")
dashboard_api.add_resource(CollectionList, "/get/clist")
dashboard_api.add_resource(UpdateCollectionList, "/update/clist")
dashboard_api.add_resource(PlanUpdate, "/planUpdate")
dashboard_api.add_resource(Quotation, "/quotation")
dashboard_api.add_resource(ClientDetails, "/get/client/<ut>")
dashboard_api.add_resource(DeleteClient, "/delete/client")
dashboard_api.add_resource(AdminCensus, "/admin/census/<uid>/<gType>")
dashboard_api.add_resource(ClientSchedule, "/client/schedule/<uid>")
dashboard_api.add_resource(Ping, "/ping")
