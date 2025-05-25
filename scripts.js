const privacy_modifier_names = ["children", "region_spec", "history"];
const lang_names = ["elementary", "middle", "high", "university", "teacher", "monkey"];
function getIp(){
    let ip = "";
    const request = new XMLHttpRequest();
    request.onreadystatechange = function (){
        if (this.readyState == 4){
            ip = this.responseText;
        }
    }
    request.open("GET", "https://api.ipify.org", false);
    request.send();
    return ip;
}

function getTextboxContentById(id){
    let textbox = document.getElementById(id);
    return textbox.value;
}

function loadRequest(link) {
    const request = new XMLHttpRequest();
    disable_submit_button();
    request.onreadystatechange = function() {
        if (this.readyState == 4){
            if (this.status == 200) {
            let result = this.responseText;
                document.getElementById("result").innerHTML = this.responseText.replace(/"/gi, "");
                enable_submit_button()
            }
            else {
                document.getElementById("result").innerHTML = "Something went wrong";
            }

        }
        else{
            document.getElementById("result").innerHTML = "<div id='thinking'></div>";
        }
}
    if (link != ""){
        // let request_text = "/requests/?link=" + link + "&ip=" + getIp();
        let request_text = ""
        if (document.getElementById("tos").checked){
            request_text += "/server/tos/?link=" + link + "&ip=" + getIp();
        }
        else{
            request_text += "/server/privacy-policy/?link=" + link + "&ip=" + getIp();
        }


        if (document.getElementById("tldr").checked){
            request_text += "&short=true";
        }

        if (document.getElementById("privacy").checked){
            for (let item of privacy_modifier_names){
                element = document.getElementById(item);
                if (element.checked){
                    request_text += "&modifiers=" + item;
                }
            }
        }

        for (let item of lang_names){
            let element = document.getElementById(item);
            if (element.checked){
                request_text += "&lang=" + item;
            }
        }
        request.open("GET", request_text, true);
        request.send();
    }

}


function disable_submit_button(){
    let button = document.getElementById("submit-button");
    button.disabled = true;
}

function enable_submit_button(){
    let button = document.getElementById("submit-button");
    button.disabled = false;
}

function disable_privacy_mods(){
    for (let item of privacy_modifier_names){
        document.getElementById(item).disabled = true;
    }
}

function enable_privacy_mods(){
    for (let item of privacy_modifier_names){
        document.getElementById(item).disabled = false;
    }
}
