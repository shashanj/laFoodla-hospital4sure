from django.forms import ModelForm
from auths.models import BloodBankUser as bb

class Bloodbank(ModelForm):
	class Meta:
		model = bb
		fields = [ 'Aplus','Aminus','Bplus', 'Bminus', 'ABplus','ABminus','Oplus','Ominus',
					'ffp','plt','cry','lpl','aph','unt','caplus','caminus','cbplus','cbminus',
					'cabplus','cabminus','coplus','cominus']
