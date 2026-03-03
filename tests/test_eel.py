import eel
import bottle

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    return bottle.static_file(filepath, root='./media')

print("Bottle route added")
