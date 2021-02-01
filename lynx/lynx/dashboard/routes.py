from flask import render_template, redirect, url_for, request, flash, redirect
from lynx.dashboard import bpDasboard
import datetime
from flask_login import login_required, current_user
from flask import current_app as app
from lynx.dataaccess.dashboardDAO import getWalletInfo
from lynx.dashboard.models import Dashboard
from lynx.wallet.wallet import getWalletTokenBalance, getEthBalance
from lynx.wallet.compound import getCompaundBalance, getUserTransactions, getTokenAPR
from lynx.wallet.models import LynxWall
from lynx.auth.models import User

@bpDasboard.route('/dashboard')
@login_required
def dashboard():
    try:
        showWalletInfo = request.args.get('show') or ''

        erc20_symbol = app.config['SYMB']
        wall = getWalletInfo(current_user.id)
        dashboard_data = getCompaundBalance(wall.Address, erc20_symbol)
        apy = getTokenAPR(erc20_symbol)
        dashboard_data.apy = str(round(apy, 2)) 

        erc20_balance = ''
        ethBalance = ''
        if showWalletInfo.upper() == 'Y':
            erc20_balance = str(getWalletTokenBalance(wall.Address, erc20_symbol)) + ' ' + erc20_symbol
            ethBalance = str(getEthBalance(wall.Address)) + ' ETH'

        trans_data = getUserTransactions(wall.Address, erc20_symbol)

        return render_template('dashboard/dashboard.html', data = dashboard_data, transactionList = trans_data, 
                                    ad = wall.Address, tokenbalance = erc20_balance, ethbalance = ethBalance, 
                                    showAddr = showWalletInfo.upper())
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))
