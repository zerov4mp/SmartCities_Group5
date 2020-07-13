async function loadMesh(path) {
    var loader = new THREE.GLTFLoader();
    var mesh;

    let promise = new Promise(function (resolve, reject) {
        loader.load(path,

            function (gltf) {
                gltf.animations; // Array<THREE.AnimationClip>
                gltf.scene; // THREE.Scene
                gltf.scenes; // Array<THREE.Scene>
                gltf.cameras; // Array<THREE.Camera>
                gltf.asset; // Object
                mesh = gltf.scene.children[0];
                resolve(mesh);
            },
            // called while loading is progressing
            function (xhr) {
                console.log((xhr.loaded / xhr.total * 100) + '% loaded');
            },
            // called when loading has errors
            function (error) {
                console.log('An error happened');
                reject("An error happened!");
            });
    });

    return await promise;
}