let formEl,
    previewEl,
    thElm,
    startOffset,
    dirTree,
    dirHolder,
    dirSubmit,
    dirPath,
    requestSent;

let dirI = 0;
let currSelected = null;
let currUL = null;
let currRows = [];

let cleanHeaders = [];

let formChanges = {
    'ids': [],
    'changes': {}
};

window.addEventListener("DOMContentLoaded", () => {
    const fileEl = document.querySelector("#file");
    const dirDialogEl = document.querySelector("#dir-modal");
    const navFileEl = document.querySelector("#nav-file");
    const dirTreeJsonEl = document.querySelector("#dir_tree_json");
    const tableBody = document.querySelector("#table-body");
    const tableHeadersJSON = document.querySelector("#colHeadsJSON");
    const tableHeaders = JSON.parse(tableHeadersJSON.getAttribute("data-json"));
    formEl = document.querySelector("#form");
    previewEl = document.querySelector("#preview");
    dirHolder = document.querySelector("#dir_holder");
    dirSubmit = document.querySelector("#dir-submit");
    dirPath = document.querySelector("#dir-path");

    dirTree = JSON.parse(dirTreeJsonEl.getAttribute("data-json"));
    iterateDir(dirTree, "", null);

    document.querySelector("#dummyframe").addEventListener("load", e => {
        let success = e.target.contentWindow.document.querySelector("body").textContent == "done" && requestSent ? true : false;

        if (success) {
            formChanges['ids'].forEach(trackid => {
                let trackRow;

                document.querySelectorAll(".data-row").forEach(entry => {
                    if (entry.querySelector('[role="trackid"]').textContent == trackid) {
                        trackRow = entry;
                    }
                });

                for (const [key, value] of Object.entries(formChanges.changes)) {
                    if (key == "file") {
                        trackRow.querySelector('[role="artwork"]').textContent = formEl.querySelector("#preview").style["background-image"];
                        trackRow.querySelector('[role="artwork"]').setAttribute("blobbed", true);
                    } else {
                        trackRow.querySelectorAll(".entry").forEach(entry => {
                            if (entry.getAttribute("fieldmap") == key) {
                                entry.textContent = value;
                            }
                        });
                    }
                }
            });

            formChanges = {
                'ids': [],
                'changes': {}
            };
            requestSent = false;
        }
    });

    tableHeaders.forEach(header => {
        let cleanHeader = header.toLowerCase();
        cleanHeader = cleanHeader.replace(" ", "");

        switch (cleanHeader) {
            case "filename":
                cleanHeader = "path"
                break;
            case "track":
                cleanHeader = "tracknumber"
                break;
            case "title":
                cleanHeader = "tracktitle"
                break;
            case "codec":
                cleanHeader = "#codec"
                break;
            case "length":
                cleanHeader = "#length"
                break;
            case "frequency":
                cleanHeader = "#samplerate"
                break;
            case "bitrate":
                cleanHeader = "#bitspersample"
                break;
        }

        cleanHeaders.push(cleanHeader);
    });

    fileEl.addEventListener("change", handleFiles, false);
    formEl.addEventListener("submit", (e) => {
        formEl.querySelector('[name="json"]').value = JSON.stringify(formChanges);
        requestSent = true;
    });
    formEl.addEventListener("change", e => {
        formChanges['ids'].includes(formEl.querySelector('[name="trackid"]').value) ? null : formChanges['ids'].push(formEl.querySelector('[name="trackid"]').value);
        formChanges['changes'][e.target.name] = e.target.value;
    });
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
            path = "";
        }

        let xmlhttp = new XMLHttpRequest();
        let theUrl = "/change-dir";
        xmlhttp.onreadystatechange = () => {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                tableBody.innerHTML = '';

                for (const [key, value] of Object.entries(JSON.parse(xmlhttp.responseText)["tracks"])) {
                    renderTableRow(key, value, JSON.parse(xmlhttp.responseText)["artworks"], tableBody);
                    dirDialogEl.close();
                }
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
            let grip = document.createElement('div');
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

function renderTableRow(rowID, rowVals, artworks, tableBody) {
    let newRow = document.createElement("tr");
    newRow.classList.add("data-row");
    let idEntry = document.createElement("td");
    idEntry.setAttribute("role", "trackid");
    idEntry.style.display = "none";
    idEntry.style.visibility = "hidden";
    idEntry.textContent = rowID;
    newRow.appendChild(idEntry);

    let artworkEntry = document.createElement("td");
    artworkEntry.style.display = "none";
    artworkEntry.style.visibility = "hidden";
    artworkEntry.setAttribute("role", "artwork");
    artworkEntry.textContent = artworks[rowVals["artwork"]].data;
    newRow.appendChild(artworkEntry);

    cleanHeaders.forEach(cleanHeader => {
        let entry = document.createElement("td");
        entry.classList.add("entry");
        entry.setAttribute("fieldmap", cleanHeader);
        entry.textContent = rowVals[cleanHeader];
        newRow.appendChild(entry);
    });

    newRow.addEventListener("click", e => {
        if (currRows.length > 0) {
            currRows.forEach(row => {
                row.classList.remove("selected");
                currRows.pop(row);
            });
        }

        currRows.push(newRow);
        newRow.classList.add("selected");

        let str = newRow.querySelector('[role="artwork"]').textContent;
        if (newRow.querySelector('[role="artwork"]').getAttribute("blobbed") != "true") {
            formEl.querySelector("#preview").style["background-image"] = "url(data:image/png;base64," + str.substring(2, str.length - 1) + ")";
        } else {
            formEl.querySelector("#preview").style["background-image"] = str;
        }
        formEl.querySelector('[name="trackid"]').value = newRow.querySelector('[role="trackid"]').textContent;

        cleanHeaders.forEach(cleanHeader => {
            let val = newRow.querySelector('[fieldmap="' + cleanHeader + '"]').textContent;
            formEl.querySelector('[name="' + cleanHeader + '"]') ? formEl.querySelector('[name="' + cleanHeader + '"]').value = val : null;
        });
    });

    tableBody.appendChild(newRow);
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