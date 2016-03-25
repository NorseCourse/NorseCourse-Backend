document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('getSavedSchedule');
  button.addEventListener('click', function() {
    console.log(getSavedSchedule());
  }, false);
}, false);


// Takes a string and returns an array
function prepareForMyLutherForm(str) {
  str = str.replace(new RegExp(" ", "g"), "");
  str = str.replace(new RegExp("\n\n", "g"), ",");
  str = str.replace(new RegExp("\n", "g"), "");
  str = str.split(",");
  return str
} 

// Use JQuery to get schedule information
function getSavedSchedule() {
  var departments = $(".data__schedule__section__department").text();
  departments = prepareForMyLutherForm(departments);

  var courseNumbers = $(".data__schedule__section__course-number").text();
  courseNumbers = prepareForMyLutherForm(courseNumbers);

  var sectionNumbers = $(".data__schedule__section__section-number").text();
  sectionNumbers = prepareForMyLutherForm(sectionNumbers);

  return [departments, courseNumbers, sectionNumbers];
  // console.log([departments, courseNumbers, sectionNumbers]);
}