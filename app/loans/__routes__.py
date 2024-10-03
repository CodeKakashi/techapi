from app.loans.addDue import LoanUpdate
from . import loans_api

loans_api.add_resource(LoanUpdate, "/loans/update/<loanId>")