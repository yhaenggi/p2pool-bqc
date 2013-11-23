import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack

nets = dict(
        bbqcoin=math.Object(
        P2P_PREFIX='fde4d942'.decode('hex'),
        P2P_PORT=19323,
        ADDRESS_VERSION=85,
        RPC_PORT=19322,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bbqcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 42*100000000 >> (height + 1)//24000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='BQC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'BBQCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/BBQCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bbqcoin'), 'bbqcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://darkgamex.ch:2751/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://darkgamex.ch:2751/address/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
    ),
    bbqcoin_testnet=math.Object(
        P2P_PREFIX='fcc1b7dc'.decode('hex'),
        P2P_PORT=59333,
        ADDRESS_VERSION=25,
        RPC_PORT=59332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bqqcoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='tLTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'BBQCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/BBQCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bbqcoin'), 'bbqcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://darkgamex.ch:2751/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://darkgamex.ch:2751/address/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
