var ros;
var room_msg;
var isConnected = false;
let prevData = [null, null, null, null];

document.getElementById("connect-button").addEventListener("click", function() {
    if (isConnected) {
        disconnectFromROS();
    } else {
        connectToROS();
    }
});

// Auto-connect when the page loads
window.onload = function() {
    connectToROS();
};

function connectToROS() {
    var address = "ws://localhost:9090";
    ros = new ROSLIB.Ros({ url: address });

    ros.on('connection', function() {
        isConnected = true;
        updateButton(true);
        console.log('Connected to ROSBridge.');

        room_msg = new ROSLIB.Topic({
            ros: ros,
            name: '/room_msg',
            messageType: 'std_msgs/Int8'
        });

        move_msg = new ROSLIB.Topic({
            ros: ros,
            name: '/cmd_vel_sub',
            messageType: 'std_msgs/Int8MultiArray'
        });

        grip_msg = new ROSLIB.Topic({
            ros: ros,
            name: '/sub_abs_gripper',
            messageType: 'std_msgs/Int8MultiArray'
        });

        sub_stat = new ROSLIB.Topic({
            ros: ros,
            name: "/state_doing",
            messageType: "std_msgs/String"
        });

        sub_stat.subscribe((message) => {
            console.log("Received message:", message.data);
            const display = document.getElementById("messageDisplay");
            if (message.data!="-1") {
                display.textContent = "Robot going to " + message.data;
                } else {
                console.warn("⚠️ Element #messageDisplay not found!");
            }
        });
        sendGrip()
    });

    ros.on('error', function(error) {
        updateButton(false);
        console.error('Error connecting to ROSBridge:', error);
    });

    ros.on('close', function() {
        isConnected = false;
        updateButton(false);
        console.warn('Disconnected from ROSBridge.');
    });
}

function disconnectFromROS() {
    if (ros) {
        ros.close();
    }
}

function updateButton(connected) {
    var button = document.getElementById("connect-button");
    if (connected) {
        button.innerText = "Connected";
        button.classList.remove("disconnected");
        button.classList.add("connected");
    } else {
        button.innerText = "Connect to ROS";
        button.classList.remove("connected");
        button.classList.add("disconnected");
    }
}

function sendMessage(state) {
    if (!ros || !room_msg) {
        console.warn('Not connected to ROSBridge.');
        return;
    }

    var msg = new ROSLIB.Message({ data: state });
    room_msg.publish(msg);
    console.log('Sent message:', state);
}

function arraysEqual(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
}

function sendMove(up, left, right, down) {
    if (!ros || !move_msg) {
        console.warn("Not connected to ROSBridge.");
        return;
    }

    let data = [up, left, right, down];
    let msg = new ROSLIB.Message({ data: data });
    move_msg.publish(msg);
    console.log("Sent message:", data);
}

function sendGrip() {
    if (!ros || !grip_msg) {
        console.warn("Not connected to ROSBridge.");
        return;
    }

    let data = [
        Number(document.getElementById("x-axis").value) || 0,
        Number(document.getElementById("z-axis").value) || 0,
        Number(document.getElementById("rotate").value) || 0,
        Number(document.getElementById("pick").value) || 0,
    ];

    if (!arraysEqual(data, prevData)) {
        let msg = new ROSLIB.Message({ data: data });
        grip_msg.publish(msg);
        console.log("Sent message:", data);
        prevData = [...data];
    }
}

document.addEventListener("DOMContentLoaded", function () {
    ["x-axis", "z-axis", "rotate", "pick"].forEach(id => {
        document.getElementById(id).addEventListener("input", sendGrip);
    });
});