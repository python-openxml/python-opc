Feature: Save an OPC package
  In order to satisfy myself that python-opc might work
  As a pptx developer
  I want to see it pass a basic round-trip sanity-check

  Scenario: Round-trip a .docx file
     Given a clean working directory
      When I open a Word file
       And I save the document package
      Then I see the docx file in the working directory

  Scenario: Round-trip a .pptx file
     Given a clean working directory
      When I open a PowerPoint file
       And I save the presentation package
      Then I see the pptx file in the working directory

  Scenario: Round-trip an .xlsx file
     Given a clean working directory
      When I open an Excel file
       And I save the spreadsheet package
      Then I see the xlsx file in the working directory
