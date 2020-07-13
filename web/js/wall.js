class Wall {

    constructor() {
        this.id = "wall";
    }

    async spawn(scene, posX, posY, width, depth, height, floorLevel) {
        await Wall.init;

        var geometry = new THREE.BoxGeometry(width, height, depth);
        var material = new THREE.MeshLambertMaterial({ map: Wall.texture });
        var wall = new THREE.Mesh(geometry, material);
        wall.castShadow = true;
        wall.receiveShadow = true;
        wall.position.set(posX, floorLevel, posY);
        this.mesh = wall;
        scene.add(wall);
    }

    getPosition() {
        return this.mesh.position;
    }
}

// initialize and load static meshes used for all class instances
Wall.init = new Promise(function (resolve, reject) {
    loadTexture("textures/wall.jpg").then(function (texture) {
        Wall.texture = texture;
        Wall.texture.wrapS = THREE.RepeatWrapping;
        Wall.texture.wrapT = THREE.RepeatWrapping;
        Wall.texture.repeat.set(32, 32);
        resolve(true);
    });
});













