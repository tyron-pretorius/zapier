function getFirstEmptyRow() {
  var spr = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Submissions");
  var column = spr.getRange('A:A');
  var values = column.getValues(); // get all data in one call
  var ct = 0;
  while ( values[ct][0] != "" ) {
    ct++;
  }
  //Browser.msgBox(ct);
  return (ct+1);
}

function setValues() {
  
  var backend = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Back End");
  
  var variable_values = backend.getRange("B7").getValue();
  var body = backend.getRange("B8").getValue();
  var dbx = backend.getRange("B9").getValue();
  var subject = backend.getRange("B10").getValue();
  var utm = backend.getRange("C28").getValue();
  
  
  var row = getFirstEmptyRow();
  var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Submissions");
  
  var timestamp = submissions.getRange(row, 1);
  var variable_values_set = submissions.getRange(row, 2);
  var body_set = submissions.getRange(row, 3);
  var utm_set = submissions.getRange(row, 4);
  var dbx_set = submissions.getRange(row, 5);
  var subject_set = submissions.getRange(row, 6);
  
  timestamp.setValue(new Date().toLocaleString());
  variable_values_set.setValue(variable_values);
  body_set.setValue(body);
  utm_set.setValue(utm);
  dbx_set.setValue(dbx);
  subject_set.setValue(subject);
}
