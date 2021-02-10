from flask import render_template, redirect, url_for, request, flash, redirect
from lynx.dashboard import bpDasboard
import datetime
from flask_login import login_required, current_user
from flask import current_app as app
from lynx.dashboard.models import Dashboard
from lynx.wallet.wallet import getWalletTokenBalance, getEthBalance
from lynx.wallet.compound import getCompaundBalance, getUserTransactions, getTokenAPR
from lynx.auth.models import User, UserWallet

@bpDasboard.route('/dashboard')
@login_required
def dashboard():
    try:
        showWalletInfo = request.args.get('show') or ''

        erc20_symbol = app.config['SYMB']
        wall = UserWallet.query.filter_by(uid=current_user.id).first()
        dashboard_data = getCompaundBalance(wall.address, erc20_symbol)
        apy = getTokenAPR(erc20_symbol)
        dashboard_data.apy = str(round(apy, 2))

        erc20_balance = ''
        ethBalance = ''
        if showWalletInfo.upper() == 'Y':
            erc20_balance = str(getWalletTokenBalance(wall.address, erc20_symbol)) + ' ' + erc20_symbol
            ethBalance = str(getEthBalance(wall.address)) + ' ETH'

        trans_data = getUserTransactions(wall.address, erc20_symbol)

        return render_template('dashboard/dashboard.html', data = dashboard_data, transactionList = trans_data, 
                                    ad = wall.address, tokenbalance = erc20_balance, ethbalance = ethBalance, 
                                    showAddr = showWalletInfo.upper())
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))
