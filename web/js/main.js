var camMinDistance = 0;
var camMaxDistance = 2000;
var camDampening = 0.05;
var maxRenderDistance = 10000;


var lb1
var lb2
var lb3
var lights

standardLight = 5.0;
standardLightBulb = 0.6;

function isJson(str) {
    if (typeof str !== 'string') return false;
    try {
        const result = JSON.parse(str);
        const type = Object.prototype.toString.call(result);
        return type === '[object Object]'
            || type === '[object Array]';
    } catch (err) {
        return false;
    }
}

        function overrideValue(){
        var id = document.getElementById("sliosID").textContent;
        var value = document.getElementById("OverrideValue").value;
        eel.eelSensorOverride(id,value);
    }

    function stopOverrideValue(){
        var id = document.getElementById("sliosID").textContent;
        eel.eelSensorOverrideStop(id);
    }

    function addPerson(){
        eel.eelAddPerson();
    }

    function removePerson(){
        eel.eelRemovePerson();
    }

    function toggleClock(){
        var c = document.getElementById("clockDiv")
        if(c.style.visibility == "hidden"){
            c.style.visibility = "visible";
        }else{
            c.style.visibility = "hidden";
        }
    }

function lightSwitch(id){
        id = id-1
        var light = lights[id]
        if(light){
            if(light.intensity == 0){
                             light.intensity = standardLightBulb
                             eel.eelLightOn(id)()
            }else{
                              light.intensity = 0
                              eel.eelLightOff(id)()
            }
        }
}

eel.expose(getLightStatus);
function getLightStatus(id){
        var light = lights[id]
        if(light){
                return light.intensity;
        }
}

eel.expose(lightOnJS);
    function lightOnJS(id){
        var light = lights[id]
        if(light){
                light.intensity = standardLightBulb
                eel.eelLightOn(id)()
        }
    }
eel.expose(lightOffJS);
    function lightOffJS(id){
        var light = lights[id]
        if(light){
            light.intensity = 0
            eel.eelLightOff(id)()
        }
    }

eel.expose(dayLightScale);
    function dayLightScale(h){
        a = -0.0005
        b = 0.0093
        c = 0.0366
        d = -0.0766

        scale = a*Math.pow(h,3) + b*Math.pow(h,2) + c*h + d

        if(scale<0){
            scale = 0
        }
        if(scale >1){
            scale = 1
        }
        return scale
    }

async function start() {

    //wait for dom to load
    document.ready = new Promise((resolve) => document.addEventListener("DOMContentLoaded", resolve));
    await document.ready;

    // GET SENSORS
    // query all sensors of the system
    // TODO: query all actuators 
    // ======================================================================================================================================
    var sensors = {};
    let sensorIds = await eel.eelGetSensors()()
    for (var i = 0; i < sensorIds.length; i++) {
        addSensor(sensorIds[i])
        sensors[sensorIds[i]] = {};
    }

    // EEL EXPOSE
    // define js functions used by python side
    // ======================================================================================================================================


    var envPlanRow = 1;
    var distPlanRow = 1;

    eel.expose(setText);
    function setText(id, text) {

        if(isJson(text)){
            msg = JSON.parse(text)

            if(msg['sender'] == "motion_sensor"){
                html = "<table>";
                for(obj in msg['data']){
                    html+= `<tr>
                               <td>
                                    ${obj}: ${msg['data'][obj]}
                               </td>
                            </tr>`
                }
                html += "</table>";
                text = html;
            }

            if(msg['sender'] == "plan_executioner"){



                html = "";
                //for(obj in msg['data']){


                    if(envPlanRow > 5){
                        for(var i = 1; i<6; i++){
                            document.getElementById("envA"+i).innerHTML = "";
                        }
                        envPlanRow = 1
                    }

                    if(distPlanRow > 5){
                        for(var i = 1; i<6; i++){
                            document.getElementById("distA"+i).innerHTML = "";
                        }
                        distPlanRow = 1
                    }

                    if(msg['data']['actuator'].includes("person")){

                        html+= `
                        <td>
                            Assign new student to chair ${msg['data']['status']}.
                        </td>
                    `
                        id = "distA"+distPlanRow
                        distPlanRow++;
                    }else{
                        //env
                        html+= `
                        <td>
                            Set actuator ${msg['data']['actuator']} to status ${msg['data']['status']}.
                        </td>
                    `
                        id = "envA"+envPlanRow
                        envPlanRow++;
                    }


                //}
                text = html;
                if(document.getElementById(id)) {
                    document.getElementById(id).innerHTML = text;
                    return
                }
            }

            if(msg['sender'] == "ContextBridge"){


                var envP = msg['data']['context_environment_problem']
                var distP = msg['data']['context_distribution_problem']


                envP = envP.substring(1,(envP.lastIndexOf(")")-1));
                distP = distP.substring(1,(distP.lastIndexOf(")")-1));;

                var regx = /\((.*?)\)/g;


                function getMatches(str,reg){
                    var listOfText = [];
                    var found;
                    while(found = reg.exec(str)) {
                        listOfText.push(found[1]);
                    };
                    return listOfText
                }

                var envPr = getMatches(envP, regx);
                var distPr = getMatches(distP, regx);

                function genTable(data){
                    html = "";

                    rest = data.length % 3;

                    for(var i=0; i<data.length; i+=3){

                        if(data.length-i == rest){

                            html += `<tr colspan="${rest}">`
                            for(var j=0; j<rest; j++){
                                html += `<td> ${data[i+j]}</td>`
                            }
                            html +=   `</tr>`

                        }else{
                            html += `<tr colspan="3">
                            <td> ${data[i]}</td>
                            <td> ${data[i+1]}</td>
                            <td> ${data[i+2]} </td>
                        </tr>`   


                        }

                    }
                    return html;
                }
                
                envPr = genTable(envPr);
                distPr = genTable(distPr);

                document.getElementById("envProblem").innerHTML = envPr;
                document.getElementById("distProblem").innerHTML = distPr;
                return


            }

        }

        if (document.getElementById(id)) {
            document.getElementById(id).innerHTML = text;
        }
        if (document.getElementById(id + "Tooltip")) {
            document.getElementById(id + "Tooltip").innerHTML = text;
        }
        if (sensors[id]) {
            sensors[id].value = text;
        }




    }

    eel.expose(setChairStatus);
    function setChairStatus(id, status) {
        if (chairs) {
            if (chairs[id]) {
                chairs[id].blob.visible = status
            }
        }
    }

    eel.expose(setSoundActuatorStatus);
    function setSoundActuatorStatus(id, status){
        if(soundActuators){
            if(soundActuators[id]){
                if(status){
                    soundActuators[id].alarm();
                }else{
                    soundActuators[id].resetAlarm();
                }
            }
        }
    }

    eel.expose(setWindowStatus);
    function setWindowStatus(id, status){
        if(windows){
            if(windows[id]){
                if(status){
                    windows[id].open();
                }else{
                    windows[id].close();
                }
            }
        }
    }

    eel.expose(setACStatus);
    function setACStatus(id,status,mode){
        if(airConditions){
            if(airConditions[id]){
                if(status){
                    airConditions[id].on();
                }else{
                    airConditions[id].off();
                }
            }
        }
    }

    eel.expose(setACMode);
    function setACMode(id,mode){
        if(airConditions){
            if(airConditions[id]){
                    if(mode){
                        airConditions[id].setHeating();
                    }else{
                        airConditions[id].setCooling();
                    }
            }
        }
    }

    eel.expose(addSensor);
    function addSensor(id) {
        document.getElementById("sensors").innerHTML += '<tr><td>' + id + '</td><td id="' + id + '"></td></tr>'
    }

    eel.expose(updateClock);
    function updateClock(dateStr){
        document.getElementById("clockDiv").innerHTML = dateStr;
    }

    // RENDERING
    // ======================================================================================================================================
    var canvasScale = 0.85;
    canvas = document.getElementById('threeContainer');
    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    var h = window.innerHeight * canvasScale;
    var w = window.innerWidth * canvasScale;
    renderer.setSize(w, h);
    renderer.domElement.setAttribute("style", "  width:100%; border-radius: 15px 50px 30px; border: 4px solid #616161; border-style: outset;");

    // RAYCASTER
    // detect objects when clicked (currently only works for pressure sensors)
    // ======================================================================================================================================
    renderer.domElement.addEventListener("click", detectObject, true);

    //onclick handler
    function detectObject(event) {
        var raycaster = new THREE.Raycaster();;
        var mouse = { x: 0, y: 0 };

        var canvasBounds = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - canvasBounds.left) / (canvasBounds.right - canvasBounds.left)) * 2 - 1;
        mouse.y = - ((event.clientY - canvasBounds.top) / (canvasBounds.bottom - canvasBounds.top)) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);

        // get objects
        objects = [];
        scene.traverse(function (node) {

            // chairs
            if (node instanceof THREE.Mesh) {
                if (node.parent && node.parent.parent && node.parent.parent.parent && node.parent.parent.parent.sliosID) {
                    objects.push(node);
                }
            }

            // sensors
            if (node instanceof THREE.Mesh) {
                if(node.sliosID){
                    objects.push(node);
                }

            }

        });

        var node = raycaster.intersectObjects(objects)[0];

        if (node && node.object) {
            node = node.object;
            var i = 0;
            while (node.parent && !node.sliosID && i < 50) {
                node = node.parent;
                i += 1;
            }


            if (node.sliosID) {

                var tooltip = document.getElementById("sensorTooltip");


                if(node.sliosID.includes("slma")){
                    node.sliosID = node.sliosID.replace("slma","slms");
                }

                if (tooltip && sensors[node.sliosID]) {


                    if(node.sliosID.includes("press")){
                        tooltip.innerHTML = `<tr>
                        <td>Name </td>
                        <td id="sliosID">${node.sliosID}</td>
                    </tr>
                    <tr>
                        <td>Current Value </td>
                        <td id="${node.sliosID}Tooltip">${sensors[node.sliosID].value}</td>
                    </tr>
                    <tr>
                        <td>Override Value</td>
                        <td>
                            <input type="text" id="OverrideValue" value="">
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <button class="menubutton" type="button" onclick="overrideValue()"> Override </button>
                        </td>
                        <td>
                            <button class="menubutton" type="button" onclick="stopOverrideValue()"> Stop override </button>
                        </td>
                    </tr>
                    `






                    }else{
                        tooltip.innerHTML = `<tr>
                        <td>Name </td>
                        <td id="sliosID">${node.sliosID}</td>
                    </tr>
                    <tr>
                        <td>Current Value </td>
                        <td id="${node.sliosID}Tooltip">${sensors[node.sliosID].value}</td>
                    </tr>
                    `
                    }




                    document.getElementById("sensorTooltipDiv").style.visibility = "visible";
                    console.log(node.sliosID);
                }



            }



        }


    }

    // ======================================================================================================================================

    // add listener on resize
    function onWindowResize() {
        var h = window.innerHeight * canvasScale;
        var w = window.innerWidth * canvasScale;
        renderer.setSize(w, h);
    }
    window.addEventListener('resize', onWindowResize, false);

    // BUILD MENU
    // ======================================================================================================================================
    document.getElementById("showSensorButton").onclick = function () {
        document.getElementById("sensorDiv").style.visibility = "visible";
    }

    document.getElementById("closeSensorButton").onclick = function () {
        document.getElementById("sensorDiv").style.visibility = "hidden";
    }

    document.getElementById("showPlanButton").onclick = function () {
        document.getElementById("planDiv").style.visibility = "visible";
    }

    document.getElementById("closePlanButton").onclick = function () {
        document.getElementById("planDiv").style.visibility = "hidden";
    }

    document.getElementById("closeSensorTooltipButton").onclick = function () {
        document.getElementById("sensorTooltipDiv").style.visibility = "hidden";
    }

    document.getElementById("addPerson").onclick = addPerson
    document.getElementById("removePerson").onclick = removePerson

    document.getElementById("toggleClock").onclick = toggleClock
    document.getElementById("clockDiv").style.visibility = "hidden"


    document.getElementById("lightSwitch1").onclick = function(){lightSwitch(1)}
    document.getElementById("lightSwitch2").onclick = function(){lightSwitch(2)}
    document.getElementById("lightSwitch3").onclick = function(){lightSwitch(3)}





    var scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, maxRenderDistance);
    camera.position.set(0, 500, 0);

    // BUILD WORLD
    // ======================================================================================================================================

    var light = new THREE.AmbientLight(0x404040, standardLight); // soft white light
    scene.add(light);

    // lighbulbs
    lb1 = new THREE.PointLight(0xffffff, 0, 0, 2);
    lb2 = new THREE.PointLight(0xffffff, 0, 0, 2);
    lb3 = new THREE.PointLight(0xffffff, 0, 0, 2);

    lb1.position.set(-400, 175, 250);
    lb2.position.set(-300, 175, -225);
    lb3.position.set(300,175,-150);

    lb1.castShadow = true
    lb2.castShadow = true
    lb3.castShadow = true

    lb1.shadow = new THREE.LightShadow(camera);
    lb2.shadow = new THREE.LightShadow(camera);
    lb3.shadow = new THREE.LightShadow(camera);

    scene.add(lb1);
    scene.add(lb2);
    scene.add(lb3);

    lights = [lb1,lb2,lb3]

    var ground = new Ground()
    ground.spawn(scene, 5000, 5000)

    var floor = new Floor()
    floor.spawn(scene, 1200, 800)

    //building
    var wall = new Wall()
    wall.spawn(scene, 0, -400, 1200, 20, 300, 0)
    wall.spawn(scene, 0, 400, 1200, 20, 300, 0)
    wall.spawn(scene, -600, 0, 20, 815, 300, 0)
    // door main
    wall.spawn(scene, 600, -250, 20, 310, 300, 0)
    wall.spawn(scene, 600, 250, 20, 310, 300, 0)

    // side walls
    wall.spawn(scene, -200, -225, 20, 350, 300, 0)
    wall.spawn(scene, -200, 225, 20, 350, 300, 0)

    // side walls 2
    wall.spawn(scene, -525, -55, 150, 20, 300, 0)
    wall.spawn(scene, -280, -55, 175, 20, 300, 0)

    // side walls 3
    wall.spawn(scene, -525, 55, 150, 20, 300, 0)
    wall.spawn(scene, -280, 55, 175, 20, 300, 0)


    // windows
    var windows = {};
    var w0 = new Window("device_w_0");
    var w1 = new Window("device_w_1");
    var w2 = new Window("device_w_2");
    windows["device_w_0"] = w0;
    windows["device_w_1"] = w1;
    windows["device_w_2"] = w2;

    w0.spawn(scene, 583, 70, -190, 300, 90);
    w1.spawn(scene, -590, 85, -220, 275, 90);
    w2.spawn(scene, -590, 85, 220, 275, 90);

    // furniture

    // sensor settings
    sensorScale = 150;
    sensorHeight = 55;


    var chairs = {};
    var airConditions = {};
    var soundActuators = {};
    var chairID = 0;
    var d = new Desk("desk");

    // room 1
    var t1Sensor = new Sensor("device_slma_0");
    soundActuators["device_slma_0"] = t1Sensor;
    d.spawn(scene, -400, 0, 300, 75, 90);
    d.spawn(scene, -400, 0, 200, 75, 90);
    t1Sensor.spawn(scene, -400,sensorHeight,250,sensorScale,90);

    var ac0 = new AC("device_cc_0")
    airConditions["device_cc_0"] = ac0;
    ac0.spawn(scene,-220,60,250,12,90);

    for (var row = 0; row < 2; row++) {
        for (var col = 0; col < 3; col++) {
            id = 'device_press_' + chairID
            chairs[id] = new Chair(id);
            chairs[id].spawn(scene, -450 + (row * 100), 0, 170 + (col * 70), 75, (row == 0 ? 90 : 270));
            chairID = chairID + 1;
        }
    }

    // room 2
    var t2Sensor = new Sensor("device_slma_1");
    soundActuators["device_slma_1"] = t1Sensor;
    d.spawn(scene, -350, 0, -200, 75, 0);
    d.spawn(scene, -450, 0, -200, 75, 0);
    d.spawn(scene, -350, 0, -250, 75, 0);
    d.spawn(scene, -450, 0, -250, 75, 0);
    t2Sensor.spawn(scene, -400, sensorHeight, -225, sensorScale ,0);

    var ac1 = new AC("device_cc_1")
    airConditions["device_cc_1"] = ac1;
    ac1.spawn(scene,-220,60,-170,12,270);


    for (var row = 0; row < 2; row++) {
        for (var col = 0; col < 3; col++) {
            id = 'device_press_' + chairID
            chairs[id] = new Chair(id);
            chairs[id].spawn(scene, -475 + (col * 80), 0, -300 + (row * 150), 75, (row == 0 ? 0 : 180));
            chairID = chairID + 1;
        }
    }

    var b = new Bookshelf("bookshelf_room2");
    b.spawn(scene, -50, 0, -390, 750, 180);

    // main room
    for (var i = 0; i < 5; i++) {
        b.spawn(scene, 250 + 130 * i, 0, -390, 750, 180);
    }

    for (var i = 0; i < 5; i++) {
        b.spawn(scene, -400 + 130 * i, 0, 390, 750, 0);
    }

    //middle row
    for (var i = 0; i < 4; i++) {
        b.spawn(scene, 350 + 130 * i, 0, 220, 750, 180);
        b.spawn(scene, 100 + (-48) - 130 * i, 0, 210, 750, 0);
        b.spawn(scene, 350 + 130 * i, 0, 70, 750, 180);
        b.spawn(scene, 100 + (-48) - 130 * i, 0, 60, 750, 0);
    }

    //main room desks long with 6 chairs
    tId = 2;
    for (var row = 0; row < 2; row++) {
        for (var col = 0; col < 3; col++) {

            tSensor = new Sensor("device_slma_"+tId)
            soundActuators["device_slma_"+tId] = tSensor;
            tId++;
            d.spawn(scene, 50 + (160 * col), 0, -250 + (150 * row), 75, 0);
            tSensor.spawn(scene, 15 + (160 * col), sensorHeight, -250 + (150 * row), sensorScale, 0)
            id = 'device_press_' + chairID
            chairs[id] = new Chair(id);
            chairs[id].spawn(scene, 65 + (160 * col), 0, -210 + (150 * row), 75, 180);
            chairID = chairID + 1;
        }
    }

    var ac2 = new AC("device_cc_2")
    airConditions["device_cc_2"] = ac2;
    ac2.spawn(scene,-180,60,-170,12,90);

    /*
    // main room desk square with 4 chairs
    for (var row = 0; row < 2; row++) {
        d.spawn(scene, -75, 0, -220 + (row * 50), 75, 0);
        for (var c = 0; c < 2; c++) {
            id = 'device_press_' + chairID
            chairs[id] = new Chair(id);
            chairs[id].spawn(scene, -95 + (50 * c), 0, -270 + (row * 150), 75, (row == 0 ? 0 : 180));
            chairID = chairID + 1;
        }
    }
    */

    // world setup complete
    // ======================================================================================================================================

    //camera.lookAt(c1.getPosition());
    canvas.appendChild(renderer.domElement);

    // controls
    //camera.position.set(0 , 0, 0);
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
    controls.dampingFactor = camDampening;
    controls.screenSpacePanning = false;
    controls.minDistance = camMinDistance;
    controls.maxDistance = camMaxDistance;
    controls.maxPolarAngle = Math.PI / 2;
    controls.target.set(0, 0, 0);

    //update daylight




    function setDaylight(){
        dateStr = document.getElementById("clockDiv").textContent;
        h = parseInt(dateStr.substring(13,15));
        m = parseInt(dateStr.substring(16,18));
        h += m/60;

        light.intensity = standardLight * dayLightScale(h);
    }

    function animate() {

        for (ac in airConditions){
            airConditions[ac].updateParticles();
        }

        requestAnimationFrame(animate);
        // update camera controls

        setDaylight();



        controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
        renderer.render(scene, camera);
    }
    animate();
}
start();

