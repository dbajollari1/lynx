from flask import render_template, redirect, url_for, request, flash, redirect
from lynx.products import bpProducts
from lynx.products.forms import SendForm, InvestForm
import datetime
from flask_login import login_required, current_user
from flask import current_app as app
from lynx.wallet.compound import getCompaundBalance, mintErcToken, redeemErcToken
from lynx.wallet.wallet import getWalletTokenBalance, transferERCToken
from lynx.auth.models import User, UserWallet
from lynx.wallet.uniswap import tradeToken

@bpProducts.route('/deposit', methods=['POST'])
@login_required
def deposit():
    try:
        amt = 0
        try:
            amt = int(request.form.get('amount'))
        except:
            flash('Amount must be numeric')
            return redirect(url_for('home'))

        erc20_symbol = app.config['SYMB']
        wall = UserWallet.query.filter_by(uid=current_user.id).first()
        balance = getWalletTokenBalance(wall.address, erc20_symbol)

        if balance < amt:
            flash('Insuficent funds')
            return redirect(url_for('home'))

        ret = mintErcToken(amt, erc20_symbol, wall)
        if str(ret).startswith("Error"):
            flash(ret)
            return redirect(url_for('home'))

        return render_template('products/deposit.html')
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

@bpProducts.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    try:
        amt = 0
        try:
            amt = int(request.form.get('wamount'))
        except:
            flash('Amount must be numeric')
            return redirect(url_for('home'))

        erc20_symbol = app.config['SYMB']
        wall = UserWallet.query.filter_by(uid=current_user.id).first()
        compBalance = getCompaundBalance(wall.address, erc20_symbol)

        if compBalance.current_balance < amt:
            flash('Insuficent funds')
            return redirect(url_for('home'))

        ret = redeemErcToken(amt, erc20_symbol, wall)
        if str(ret).startswith("Error"):
            flash(ret)
            return redirect(url_for('home'))

        return render_template('products/withdraw.html')
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))


@bpProducts.route('/pinvest', methods=['GET', 'POST'])
@login_required
def pinvest():
    frm = InvestForm(request.form)
    tokens = []
    try:
        for tkn in app.config['TOKENS'].items(): # items gives both: app.config['LANGUAGES'].keys() and .values()
            tokens.append(tkn)
        frm.Token.choices = tokens
        
        if request.method == 'POST':
            if frm.validate():
                userWall = UserWallet.query.filter_by(uid=current_user.id).first()
                selected_token = frm.Token.data # request.form.get('language')
                amount_token = frm.Amount.data
                tradeToken(selected_token, amount_token, userWall)
                flash("Trade Successfull")
        return render_template('products/pinvest.html', form = frm)
    except Exception as e:
        app.logger.error(str(e))
        return redirect(url_for('errors.error')) 


@bpProducts.route('/psend', methods=['GET', 'POST'])
@login_required
def psend():
    tr_form = SendForm(request.form)
    tr_form.tokenSymbol.data = app.config['SYMB']
    try:
        if request.method == 'POST':
            if tr_form.validate():
                user1 = User.query.filter_by(email=tr_form.fromemail.data).first()
                if not user1:
                    flash('Invalid from user')
                    return render_template('products/psend.html',form=tr_form)

                user2 = User.query.filter_by(email=tr_form.toemail.data).first()
                if not user2:
                    flash('Invalid to user')
                    return render_template('products/psend.html',form=tr_form)

                wallFrom = UserWallet.query.filter_by(uid=user1.id).first()
                wallTo = UserWallet.query.filter_by(uid=user2.id).first()
                ret = transferERCToken(wallFrom.address, wallTo.address, tr_form.amt.data, wallFrom.PrivateKey, tr_form.tokenSymbol.data)
                if str(ret).startswith("Error"):
                    flash(ret)
                else:
                    flash('Transaction completed successfully.')
                    return redirect(url_for('home'))
        else:
            tr_form.amt.data = 0

        return render_template('products/psend.html',form=tr_form)
    except Exception as e:
        app.logger.error(str(e))
        flash(str(e))
        return redirect(url_for('errors.error'))

