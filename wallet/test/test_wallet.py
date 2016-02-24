from wallet.models import StoreCard, Pass, Barcode
import json
from io import BytesIO, StringIO

organizationName = 'Sample Org'
passTypeIdentifier = 'pass.com.example'
teamIdentifier = 'ZZZ123'
passDescription = 'A Sample Pass'
serialNumber = '1234567'

def sample_store_card():
    cardInfo = StoreCard()
    cardInfo.addPrimaryField('name', 'John Doe', 'Name')
    passfile = Pass(cardInfo, \
        passTypeIdentifier=passTypeIdentifier, \
        organizationName=organizationName, \
        teamIdentifier=teamIdentifier)
    passfile.serialNumber = serialNumber
    passfile.description = passDescription
    passfile.barcode = Barcode(message = 'Barcode message')
    return passfile

def test_storecard_json():
    passfile = sample_store_card()
    passJson = passfile.json_dict()
    assert passJson is not None
    assert passJson['formatVersion'] == 1
    assert passJson['passTypeIdentifier'] == passTypeIdentifier
    assert passJson['serialNumber'] == '1234567'
    assert passJson['teamIdentifier'] == teamIdentifier
    assert passJson['organizationName'] == organizationName
    assert passJson['description'] == passDescription
    assert len(passfile._files) == 0

    # Including the icon and logo is necessary for the passbook to be valid.
    passfile.addFile('icon.png', open('wallet/test/static/icon.png', 'rb'))
    assert len(passfile._files) == 1
    assert 'icon.png' in passfile._files

def test_manifest():
    passfile = sample_store_card()
    passfile.addFile('icon.png', open('wallet/test/static/icon.png', 'rb'))
    actualJson = passfile._createManifest(passfile._createPassJson())
    actual = json.loads(actualJson.decode('utf-8'))
    assert 'pass.json' in actual

    assert '170eed23019542b0a2890a0bf753effea0db181a' == actual['icon.png']

def test_signing():
    pass
