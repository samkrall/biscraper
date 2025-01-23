from flask import Flask, render_template, flash, redirect, url_for
from forms import EmailForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '5f7430868633238cb442d608897edba6'

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        # TODO: Add email processing logic (e.g., database save, mailing list)
        flash(f'Email {email} submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('home.html', title='Home', form=form)

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run(debug=True)