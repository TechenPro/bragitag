let previewEl,
    thElm,
    startOffset,
    dirTree,
    dirHolder,
    dirSubmit,
    dirPath;

let dirI = 0;
let currSelected = null;
let currUL = null;

window.addEventListener("DOMContentLoaded", () => {
    const fileEl = document.querySelector("#file");
    const formEl = document.querySelector("#form");
    const dirDialogEl = document.querySelector("#dir-modal");
    const navFileEl = document.querySelector("#nav-file");
    const dirTreeJsonEl = document.querySelector("#dir_tree_json");
    previewEl = document.querySelector("#preview");
    dirHolder = document.querySelector("#dir_holder");
    dirSubmit = document.querySelector("#dir-submit");
    dirPath = document.querySelector("#dir-path");
    dirTree = JSON.parse(dirTreeJsonEl.getAttribute("data-json"));

    iterateDir(dirTree, "", null);

    fileEl.addEventListener("change", handleFiles, false);
    // formEl.addEventListener("submit", (e) => {

    // });
    navFileEl.addEventListener("click", () => {
        dirDialogEl.showModal();
    });
    dirSubmit.addEventListener("click", () => {
        let path = "";

        if (currSelected) {
            path = currSelected.getAttribute("path");
        } else if (currUL) {
            path = currUL.getAttribute("path");
        } else {
            path = "/";
        }

        let xmlhttp = new XMLHttpRequest();
        let theUrl = "/change-dir";
        xmlhttp.onreadystatechange = () => {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                alert(xmlhttp.responseText);
            }
        }
        xmlhttp.open("POST", theUrl);
        // xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(path);
    });

    dirDialogEl.addEventListener("click", e => {
        let contents = dirDialogEl.querySelector("#contents");
        !contents.contains(e.target) ? dirDialogEl.close() : null;
    });

    // Resizing (copied)
    Array.prototype.forEach.call(
        document.querySelectorAll("table th"),
        function (th) {
            th.style.position = 'relative';

            let grip = document.createElement('div');
            grip.innerHTML = "&nbsp;";
            grip.style.top = 0;
            grip.style.right = 0;
            grip.style.bottom = 0;
            grip.style.width = '5px';
            grip.style.position = 'absolute';
            grip.style.cursor = 'col-resize';
            grip.addEventListener('mousedown', function (e) {
                thElm = th;
                startOffset = th.offsetWidth - e.pageX;
            });

            th.appendChild(grip);
        }
    );

    document.addEventListener('mousemove', function (e) {
        if (thElm) {
            thElm.style.width = startOffset + e.pageX + 'px';
        }
    });

    document.addEventListener('mouseup', function () {
        thElm = undefined;
    });
});

function handleFiles() {
    const fileList = this.files;

    previewEl.style["background-image"] = "url(" + URL.createObjectURL(fileList[0]) + ")";
}

function iterateDir(dirMap, prefix, prevUL) {
    if (Object.keys(dirMap).length <= 0) {
        return;
    }

    let newDirUL = document.createElement("ul");
    newDirUL.classList.add("dir-list");
    dirHolder.appendChild(newDirUL);
    newDirUL.setAttribute("mapping", dirI);
    newDirUL.setAttribute("path", prefix);
    dirI++;

    if (prevUL) {
        newDirUL.setAttribute("prevUL", prevUL.getAttribute("mapping"));
        newDirUL.style.display = "none";
        let prevLI = document.createElement("li");
        prevLI.textContent = "/..";
        prevLI.classList.add("item");
        prevLI.classList.add("prev");
        prevLI.setAttribute("path", prefix);
        prevLI.addEventListener("click", e => {
            if (e.target.getAttribute("selected")) {
                e.target.removeAttribute("selected");
                currSelected = null;
                e.target.parentElement.style.display = "none";
                document.querySelector('[mapping="' + e.target.parentElement.getAttribute("prevul") + '"').style.display = "unset";
                dirPath.textContent = "/" + document.querySelector('[mapping="' + e.target.parentElement.getAttribute("prevul") + '"').getAttribute("path");
                dirSubmit.textContent = "Use Current Directory";
            } else {
                if (currSelected) {
                    currSelected.removeAttribute("selected");
                }
                e.target.setAttribute("selected", true);
                dirSubmit.textContent = "Use Current Directory";
                currSelected = e.target;
            }
        });
        newDirUL.appendChild(prevLI);
    }

    Object.keys(dirMap).forEach(key => {
        let newDirLI = document.createElement("li");
        let mapID = dirI;

        newDirLI.textContent = key;
        newDirLI.classList.add("item");
        newDirLI.setAttribute("path", prefix + key);
        Object.keys(dirMap[key]).length > 0 ? newDirLI.setAttribute("next", dirI) : null;

        newDirLI.addEventListener("click", e => {
            if (e.target.getAttribute("selected") && newDirLI.getAttribute("next")) {
                e.target.removeAttribute("selected");
                currSelected = null;
                e.target.parentElement.style.display = "none";
                currUL = document.querySelector('[mapping="' + mapID + '"');
                document.querySelector('[mapping="' + mapID + '"').style.display = "unset";
                dirPath.textContent = "/" + document.querySelector('[mapping="' + mapID + '"').getAttribute("path");
                dirSubmit.textContent = "Use Current Directory";
            } else {
                if (currSelected) {
                    currSelected.removeAttribute("selected");
                }
                e.target.setAttribute("selected", true);
                dirSubmit.textContent = "Use Selected Directory";
                currSelected = e.target;
            }
        });
        newDirUL.appendChild(newDirLI);

        Object.keys(dirMap).length > 0 ? iterateDir(dirMap[key], prefix + key + "/", newDirUL) : null;
    });
}