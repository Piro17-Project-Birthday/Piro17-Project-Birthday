function dropdown_menu() {
  let click = document.getElementById("dropdown_content");
  if (click.style.display === "none") {
    click.style.display = "block";
  } else {
    click.style.display = "none";
  }
}
