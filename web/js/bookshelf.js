class Bookshelf {

	constructor(id) {
		this.id = id;
	}

    toggle(){

    }

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await Bookshelf.init;

		var thisBookshelf = this;

		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisBookshelf.body = Bookshelf.mesh.clone();



			// assemble group
			thisBookshelf.group = new THREE.Group();
			thisBookshelf.group.add(thisBookshelf.body);

			// set in world
			thisBookshelf.group.position.set(posX, posY, posZ);
	        thisBookshelf.group.rotation.y = rotation * (Math.PI/180);

			//scale the drone to the right size
			thisBookshelf.group.scale.set(scaleXYZ, scaleXYZ, scaleXYZ);

			// add the drone to the THREE.js scene
			scene.add(thisBookshelf.group);

			//done => resolve
			resolve(true);
		})
	}

	setPosition(x, y, z) { // x=horizontal axis1,  y=vertical axis = height, z=horizontal axis2
		this.getPosition().x = x;

		if (y > this.heightMin) {
			this.getPosition().y = y;
		} else {
			this.getPosition().y = this.heightMin;
		}
		this.getPosition().z = z;
	}

	getPosition() {
		return this.group.position;
	}



}

// initialize and load static meshes used for all class instances
Bookshelf.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/bookshelf/bookshelf.gltf').then(function (bs) {
	        Bookshelf.mesh = bs;
			resolve(true);
	});
})













