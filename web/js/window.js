class Window {

	constructor(id) {
		this.id = id;
	}

    toggle(){

    }

	async spawn(scene, posX, posY, posZ, scaleXYZ, rotation) {
		await Window.init;

		var thisWindow = this;

		return new Promise(async function (resolve, reject) {

			// clone mesh
			thisWindow.body = Window.mesh.clone();

			thisWindow.body.children[0].children.splice(1,3);

			thisWindow.body.children[0].children[0].children[0].sliosID = thisWindow.id;
			thisWindow.body.children[0].children[0].children[1].sliosID = thisWindow.id;
			thisWindow.body.children[0].children[0].children[2].sliosID = thisWindow.id;

			var windowCase = new THREE.MeshLambertMaterial({map: Desk.texture });
			thisWindow.body.children[0].children[0].children[1].material = windowCase;
			thisWindow.body.children[0].children[0].children[2].material = windowCase;

			// set in world
			thisWindow.body.position.set(posX, posY, posZ);
	        thisWindow.body.rotation.y = rotation * (Math.PI/180);

			//scale the drone to the right size
			thisWindow.body.scale.set(scaleXYZ, scaleXYZ, scaleXYZ);

			// add the drone to the THREE.js scene
			scene.add(thisWindow.body);

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

	open(){
		this.body.children[0].children[0].children[0].visible = false;
	}

	close(){
		this.body.children[0].children[0].children[0].visible = true;

	}

	getPosition() {
		return this.group.position;
	}



}

// initialize and load static meshes used for all class instances
Window.init = new Promise(function (resolve, reject) {
	loadMesh('mesh/window/window.gltf').then(function (bs) {
		Window.mesh = bs;
		loadTexture("textures/wood_table.jpg").then(function (texture) {
			Window.texture = texture;
			resolve(true);
		});
	});
})













