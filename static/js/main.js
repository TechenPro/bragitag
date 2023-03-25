let previewEl;

window.addEventListener("DOMContentLoaded", () => {
    const fileEl = document.querySelector("#file");
    previewEl = document.querySelector("#preview");

    fileEl.addEventListener("change", handleFiles, false);
});

function handleFiles() {
    const fileList = this.files;

    previewEl.style["background-image"] = "url(" + URL.createObjectURL(fileList[0]) + ")";
}