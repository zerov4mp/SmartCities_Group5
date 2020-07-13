class Desk {

	constructor(id) {
		this.id = id;
	}

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await Desk.init;

		var thisDesk = this;

		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisDesk.body = Desk.mesh.clone();

            for(var i=0;i<thisDesk.body.children[0].children.length;i++){
                thisDesk.body.children[0].children[i].material = new THREE.MeshLambertMaterial({map: Desk.texture })
            }

			// assemble group
			thisDesk.group = new THREE.Group();
			thisDesk.group.add(thisDesk.body);


			// set in world
			thisDesk.group.position.set(posX, posY, posZ);
	        thisDesk.group.rotation.y = rotation * (Math.PI/180);

			thisDesk.group.scale.set(scaleXYZ, scaleXYZ, scaleXYZ);
			scene.add(thisDesk.group);

			// add sound actuator/sensor to table
			


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
Desk.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/desk/desk.gltf').then(function (desk) {
	        Desk.mesh = desk;
	        loadTexture("textures/wood_table.jpg").then(function (texture) {
	            Desk.texture = texture;
	            resolve(true);
	        });
	});
})













