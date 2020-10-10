
//see https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
function lightenDarkenColor(col,amt) {
    var usePound = false;
    if ( col[0] == "#" ) {
        col = col.slice(1);
        usePound = true;
    }
    var num = parseInt(col,16),
        validate = function(v){ return v > 255 ? 255 : v < 0 ? 0 : v; },
        r = validate((num >> 16) + amt),
        b = validate(((num >> 8) & 0x00FF) + amt),
        g = validate((num & 0x0000FF) + amt);

    return (usePound ? "#" : "") + (g | (b << 8) | (r << 16)).toString(16);
}
