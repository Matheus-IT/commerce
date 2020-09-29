from django import forms

class AddBidForm(forms.Form):
	newBidValue = forms.DecimalField(
		widget=forms.NumberInput(attrs={ 'class': 'form-control', 'placeholder': 'Bid...' }),
		label='Your bid goes here', 
		max_digits=10, 
		decimal_places=2, 
		min_value=0,
	)
	prefix = 'bidForm_pre'


class AddCommentForm(forms.Form):
	newCommentValue = forms.CharField(
		widget=forms.Textarea(attrs={ 
			'class': 'newComment', 
			'placeholder': 'Add a comment...', 
			'cols': '90', 
			'rows': '7' 
		}),
		label=False,
		max_length=1024,
	)
	prefix = 'commentForm_pre'
