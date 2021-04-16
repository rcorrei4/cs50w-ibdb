from django import forms

CHOICES = [('1', '☆'),
		   ('2', '☆'),
		   ('3', '☆'),
		   ('4', '☆'),
		   ('5', '☆'),]

class ReviewForm(forms.Form):
	rating = forms.ChoiceField(choices=CHOICES)
	title = forms.CharField(max_length=175)
	text = forms.CharField(max_length=500)