function triggerForNesting() {
  

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Customer Database Large");

  var rows = sheet.getDataRange().getValues();
      
  var url = "https://hooks.zapier.com/hooks/catch/65051/bydbbeq"
  var options = {
    "method": "post",
    "headers": {},
    "payload": {
      "length": rows.length,
      "index_start":2,
      "index_end":501
    }
  };
  
  var response = UrlFetchApp.fetch(url, options);
 
}
