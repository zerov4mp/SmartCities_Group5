// instantiate a loader
function loadTexture(file) {
    return new Promise(function (resolve, reject) {
        var loader = new THREE.TextureLoader();
        // load a resource
        loader.load(
            // resource URL
            file,

            // onLoad callback
            function (texture) {
                // in this example we create the material when the texture is loaded
                resolve(texture)
                /*var material = new THREE.MeshBasicMaterial( {
                    map: texture
                 } );
                */
            },

            // onProgress callback currently not supported
            undefined,

            // onError callback
            function (err) {
                console.error('An error happened.');
            }
        );
    })
}






