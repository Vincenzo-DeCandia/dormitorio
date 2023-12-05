let first_elem_navBar;
let styles;
let Modal;


// If resolution is < ...px by clicking on telephone/position icon it will open a new window.
function checkResolution(type) {
    if (type === "telephone") {
        // Open modal telephone
        first_elem_navBar = document.getElementById('telephone');
        styles = window.getComputedStyle(first_elem_navBar);

        // Check if the telephone number is displayed
        if (styles.display === "none") {
            Modal = new bootstrap.Modal(document.getElementById("modalTelephone"));
            Modal.show();
        }
    } else if (type === "position") {
        //Open modal position
        first_elem_navBar = document.getElementById('position');
        styles = window.getComputedStyle(first_elem_navBar);

        // Check if the position is displayed
        if (styles.display === "none") {
            Modal = new bootstrap.Modal(document.getElementById("modalPosition"));
            Modal.show();
        }
    } else if (type === "positionClose" || type === "telephoneClose") {
        Modal.hide();
    }
}
// End checkResolution function

