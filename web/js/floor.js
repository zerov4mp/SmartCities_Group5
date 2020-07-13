class Floor {

	constructor() {
		this.id = "floor";
	}

	async spawn(scene, dimX, dimY) {
		await Floor.init;

        var geometry = new THREE.BoxGeometry( dimX, 1, dimY);
        var material = new THREE.MeshLambertMaterial( {map: Floor.texture} );
        var floor = new THREE.Mesh( geometry, material );
        floor.position.set(0,-1,0);
        floor.receiveShadow = true;
        this.mesh = floor;
        scene.add(floor);
	}

	getPosition() {
		return this.mesh.position;
	}
}

// initialize and load static meshes used for all class instances
Floor.init = new Promise(function (resolve, reject) {
    loadTexture("textures/wood.jpg").then(function(texture){
    Floor.texture = texture;
    Floor.texture.wrapS = THREE.RepeatWrapping;
    Floor.texture.wrapT = THREE.RepeatWrapping;
    Floor.texture.repeat.set( 32, 32 );
    resolve(true);
    });
});













