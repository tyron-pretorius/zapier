function setValues() {
  
  var backend = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Back End");
  
  var variable_values = backend.getRange("B7").getValue();
  var subject_line = backend.getRange("B8").getValue();
  var dropbox_values = backend.getRange("B9").getValue();
  var dynamic_values = backend.getRange("B10").getValue();
 
  var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Submissions");
  var row = submissions.getLastRow() + 1;
  
  
  var timestamp = submissions.getRange(row, 1);
  var variable_values_set = submissions.getRange(row, 2);
  var subject_line_set = submissions.getRange(row, 3);
  var dropbox_values_set = submissions.getRange(row, 4);
  var dynamic_values_set = submissions.getRange(row, 5);
  
  timestamp.setValue(new Date().toLocaleString());
  variable_values_set.setValue(variable_values);
  subject_line_set.setValue('\''+ subject_line);
  dropbox_values_set.setValue(dropbox_values);
  dynamic_values_set.setValue(dynamic_values);
}
