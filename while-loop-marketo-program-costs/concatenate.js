function setValues() {
  
  //Point variable to the active sheet i.e.the one that the submit button is pressed on
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  //Get number of programs that need updating
  var lastRow = sheet.getLastRow();
  
  //Get arrays of values from the cost and program columns
  var program_values = sheet.getRange("A2:A"+lastRow).getValues();
  var cost_values = sheet.getRange("B2:B"+lastRow).getValues();
  
  //Create a string from each array so that they can each be submitted to a single cell
  var costs_string = cost_values.join("*");
  var programs_string = program_values.join("*");
  
  //Point variable to the "Cost Submissions" sheet and get first empty row
  var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Marketo Program Period Cost Submissions");
  var row = submissions.getLastRow() + 1;

  //Point variables to 4 cells in the first empty row
  var timestamp = submissions.getRange(row, 1);
  var costs = submissions.getRange(row, 2);
  var programs = submissions.getRange(row, 3);
  var log = submissions.getRange(row, 4);
  
  //Get the date and timestamp
  var ts = new Date().toLocaleString()
  
  //Set the values of the 4 cells in  the first empty row
  timestamp.setValue(ts);
  costs.setValue(costs_string);
  programs.setValue(programs_string);
  log.setValue(ts + ':')
  
  //Setup the webhook destination and payload
  var url = "https://hooks.zapier.com/hooks/catch/###/###/";
  var options = {
    "method": "post",
    "headers": {},
    "payload": {
      "Index": '0',
      "Timestamp": ts
    }
  };
  
  //Send a webhook to trigger the zap and store the response
  var response = UrlFetchApp.fetch(url, options);
  
}
