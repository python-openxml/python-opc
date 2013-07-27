Feature: Save an OPC package
  In order to satisfy myself that python-opc might work
  As a pptx developer
  I want to see it pass a basic round-trip sanity-check

  Scenario: Round-trip a .pptx file
     Given a clean working directory
      When I open a PowerPoint file
       And I save the presentation package
      Then I see the pptx file in the working directory
