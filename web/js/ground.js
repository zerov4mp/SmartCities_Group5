class Ground {

    constructor() {
        this.id = "ground";
    }

    async spawn(scene, dimX, dimY) {
        await Ground.init;

        var geometry = new THREE.BoxGeometry(dimX, 1, dimY);
        var material = new THREE.MeshLambertMaterial({ map: Ground.texture });
        var ground = new THREE.Mesh(geometry, material);
        ground.position.set(0, -2, 0)
        this.mesh = ground;
        scene.add(ground);
    }

    getPosition() {
        return this.mesh.position;
    }
}

// initialize and load static meshes used for all class instances
Ground.init = new Promise(function (resolve, reject) {
    loadTexture("textures/grass.jpg").then(function (texture) {
        Ground.texture = texture;
        Ground.texture.wrapS = THREE.RepeatWrapping;
        Ground.texture.wrapT = THREE.RepeatWrapping;
        Ground.texture.repeat.set(64, 64);
        resolve(true);
    });
});













