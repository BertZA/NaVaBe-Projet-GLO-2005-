from flask import Flask, render_template, request, url_for, redirect, flash
from static.script.ConnectionUtils import is_client_connectable, generate_pass

Token = ''
app = Flask(__name__)


# Token de page appellant. Attribué aléatoirement
@app.route('/')
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    """
     Affiche la page de bienvenue de note site
    :return: welcome.html
    """
    return render_template('welcome.html')


@app.route('/login', methods=['POST', 'GET'])
def login(msg: str = ""):
    """
    Login du client sur notre site
    :return: sign-in.html
    """
    if not request.args.get('msg') is None:
        msg = request.args.get('msg')
    return render_template('login.html', MsgError=msg)


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    """
    Inscription du client de notre site
    :return: sign-in.html
    """

    option = 'disabled'
    msg_for_name = "Nom et nom de famille"
    msg_for_date = "Date de naissance"
    demande_NEQ = ''
    demande_prod = ''

    submit_page = request.form.get('name_page')
    if not submit_page is None:
        if request.form.get('type_account') == 'producteur':
            msg_for_name = "Nom de l'entreprise"
            msg_for_date = "Date d'enregistrement au registre du Québec"
            option = 'enabled required'
            demande_NEQ = "Numéro d'entreprise du Québec"
            demande_prod = "Description de votre production"

    return render_template('sign-in.html',
                           option_=option,
                           Msg_nom=msg_for_name,
                           Msg_annee=msg_for_date,
                           demande_prod=demande_prod,
                           demande_NEQ=demande_NEQ)


@app.route('/submit', methods=['POST'])
def submit():
    """
    Vérification des données fournit sur le site lors du login ou/et de l'inscription
    @login : - page demandant soumission : login.html
             - page d'après : main.html
    @signin : - page demandant soumission : sign-in.html
             - page d'après : welcome.html (avec un message)

    @Auteur : Bertrand A

    :return: La page qui demande la soumission si les infos ne sont pas correctes
             la page d'après soumission sinon.

    """
    submit_page = request.form.get('name_page')
    global Token
    if submit_page == 'login':
        """
        Routine de traitement pour la connexion
        """
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        Token = generate_pass(10, True)
        if not is_client_connectable(email, password):
            return redirect(url_for('login', msg="Courriel ou Mot de passe invalide"))
        return redirect(url_for('main', caller="submit", token=Token))

    if submit_page == 'sign-in':
        """
        Routine de traitement pour l'enregistrement 
        """
        pass
    return ' '


@app.route('/main', methods=['POST', 'GET'])
def main(caller: str = "", token: str = ''):
    """
    Cette fonction doit permettre à l'utilisateur de naviguer sur NaVaBe, une fois ce dernier connecté.
    La Page html renvoyé est le tableau de bord du site.
    L'utilisateur doit être capable de faire de recherches, voir le profil d'un producteur ou d'un autre user
    Laisser un commentaire sur les autres (et voir exprimer sa satisfaction aussi) etc ...
    Cette fonction peut utiliser d'autres fonctions qui doivent être créé dans le dossier script.

    @Auteur : Bertrand A

    :return: main.html
    """
    if not request.args.get('caller') is None:
        caller = request.args.get('caller')
        token = request.args.get('token')

        if caller == 'submit':
            print(caller)
            if token == Token:
                return render_template('main.html', Name_menu='Tableau de bord')
    return "<h1> Vous devez vous authentifié pour accéder à la suite du site </h1>"


@app.route('/password_recovery')
def password_recovery():
    return render_template('password-recovery.html')


if __name__ == '__main__':
    app.run(debug=True)
