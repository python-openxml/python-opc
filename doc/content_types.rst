###########################
Content type constant names
###########################

The following names are defined in the :mod:`opc.constants` module to allow
content types to be referenced using an identifier rather than a literal
value.

The following import statement makes these available in a module::

    from opc.constants import CONTENT_TYPE as CT

A content type may then be referenced as a member of ``CT`` using dotted
notation, for example::

    part.content_type = CT.PML_SLIDE_LAYOUT

The content type names are determined by transforming the trailing text of
the content type string to upper snake case, replacing illegal Python
identifier characters (dash and period) with an underscore, and prefixing one
of these seven namespace abbreviations:

* **DML** -- DrawingML
* **OFC** -- Microsoft Office document
* **OPC** -- Open Packaging Convention
* **PML** -- PresentationML
* **SML** -- SpreadsheetML
* **WML** -- WordprocessingML
* no prefix -- standard MIME types, such as those used for image formats like
  JPEG

BMP
    image/bmp

DML_CHART
    application/vnd.openxmlformats-officedocument.drawingml.chart+xml

DML_CHARTSHAPES
    application/vnd.openxmlformats-officedocument.drawingml.chartshapes+xml

DML_DIAGRAM_COLORS
    application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml

DML_DIAGRAM_DATA
    application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml

DML_DIAGRAM_LAYOUT
    application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml

DML_DIAGRAM_STYLE
    application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml

GIF
    image/gif

JPEG
    image/jpeg

MS_PHOTO
    image/vnd.ms-photo

OFC_CUSTOM_PROPERTIES
    application/vnd.openxmlformats-officedocument.custom-properties+xml

OFC_CUSTOM_XML_PROPERTIES
    application/vnd.openxmlformats-officedocument.customXmlProperties+xml

OFC_DRAWING
    application/vnd.openxmlformats-officedocument.drawing+xml

OFC_EXTENDED_PROPERTIES
    application/vnd.openxmlformats-officedocument.extended-properties+xml

OFC_OLE_OBJECT
    application/vnd.openxmlformats-officedocument.oleObject

OFC_PACKAGE
    application/vnd.openxmlformats-officedocument.package

OFC_THEME
    application/vnd.openxmlformats-officedocument.theme+xml

OFC_THEME_OVERRIDE
    application/vnd.openxmlformats-officedocument.themeOverride+xml

OFC_VML_DRAWING
    application/vnd.openxmlformats-officedocument.vmlDrawing

OPC_CORE_PROPERTIES
    application/vnd.openxmlformats-package.core-properties+xml

OPC_DIGITAL_SIGNATURE_CERTIFICATE
    application/vnd.openxmlformats-package.digital-signature-certificate

OPC_DIGITAL_SIGNATURE_ORIGIN
    application/vnd.openxmlformats-package.digital-signature-origin

OPC_DIGITAL_SIGNATURE_XMLSIGNATURE
    application/vnd.openxmlformats-package.digital-signature-xmlsignature+xml

OPC_RELATIONSHIPS
    application/vnd.openxmlformats-package.relationships+xml

PML_COMMENTS
    application/vnd.openxmlformats-officedocument.presentationml.comments+xml

PML_COMMENT_AUTHORS
    application/vnd.openxmlformats-officedocument.presentationml.commentAuthors+xml

PML_HANDOUT_MASTER
    application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml

PML_NOTES_MASTER
    application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml

PML_NOTES_SLIDE
    application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml

PML_PRESENTATION_MAIN
    application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml

PML_PRES_PROPS
    application/vnd.openxmlformats-officedocument.presentationml.presProps+xml

PML_PRINTER_SETTINGS
    application/vnd.openxmlformats-officedocument.presentationml.printerSettings

PML_SLIDE
    application/vnd.openxmlformats-officedocument.presentationml.slide+xml

PML_SLIDESHOW_MAIN
    application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml

PML_SLIDE_LAYOUT
    application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml

PML_SLIDE_MASTER
    application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml

PML_SLIDE_UPDATE_INFO
    application/vnd.openxmlformats-officedocument.presentationml.slideUpdateInfo+xml

PML_TABLE_STYLES
    application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml

PML_TAGS
    application/vnd.openxmlformats-officedocument.presentationml.tags+xml

PML_TEMPLATE_MAIN
    application/vnd.openxmlformats-officedocument.presentationml.template.main+xml

PML_VIEW_PROPS
    application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml

PNG
    image/png

SML_CALC_CHAIN
    application/vnd.openxmlformats-officedocument.spreadsheetml.calcChain+xml

SML_CHARTSHEET
    application/vnd.openxmlformats-officedocument.spreadsheetml.chartsheet+xml

SML_COMMENTS
    application/vnd.openxmlformats-officedocument.spreadsheetml.comments+xml

SML_CONNECTIONS
    application/vnd.openxmlformats-officedocument.spreadsheetml.connections+xml

SML_CUSTOM_PROPERTY
    application/vnd.openxmlformats-officedocument.spreadsheetml.customProperty

SML_DIALOGSHEET
    application/vnd.openxmlformats-officedocument.spreadsheetml.dialogsheet+xml

SML_EXTERNAL_LINK
    application/vnd.openxmlformats-officedocument.spreadsheetml.externalLink+xml

SML_PIVOT_CACHE_DEFINITION
    application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheDefinition+xml

SML_PIVOT_CACHE_RECORDS
    application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheRecords+xml

SML_PIVOT_TABLE
    application/vnd.openxmlformats-officedocument.spreadsheetml.pivotTable+xml

SML_PRINTER_SETTINGS
    application/vnd.openxmlformats-officedocument.spreadsheetml.printerSettings

SML_QUERY_TABLE
    application/vnd.openxmlformats-officedocument.spreadsheetml.queryTable+xml

SML_REVISION_HEADERS
    application/vnd.openxmlformats-officedocument.spreadsheetml.revisionHeaders+xml

SML_REVISION_LOG
    application/vnd.openxmlformats-officedocument.spreadsheetml.revisionLog+xml

SML_SHARED_STRINGS
    application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml

SML_SHEET
    application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

SML_SHEET_METADATA
    application/vnd.openxmlformats-officedocument.spreadsheetml.sheetMetadata+xml

SML_STYLES
    application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml

SML_TABLE
    application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml

SML_TABLE_SINGLE_CELLS
    application/vnd.openxmlformats-officedocument.spreadsheetml.tableSingleCells+xml

SML_USER_NAMES
    application/vnd.openxmlformats-officedocument.spreadsheetml.userNames+xml

SML_VOLATILE_DEPENDENCIES
    application/vnd.openxmlformats-officedocument.spreadsheetml.volatileDependencies+xml

SML_WORKSHEET
    application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml

TIFF
    image/tiff

WML_COMMENTS
    application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml

WML_DOCUMENT_GLOSSARY
    application/vnd.openxmlformats-officedocument.wordprocessingml.document.glossary+xml

WML_DOCUMENT_MAIN
    application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml

WML_ENDNOTES
    application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml

WML_FONT_TABLE
    application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml

WML_FOOTER
    application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml

WML_FOOTNOTES
    application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml

WML_HEADER
    application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml

WML_NUMBERING
    application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml

WML_PRINTER_SETTINGS
    application/vnd.openxmlformats-officedocument.wordprocessingml.printerSettings

WML_SETTINGS
    application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml

WML_STYLES
    application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml

WML_WEB_SETTINGS
    application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml

XML
    application/xml

X_EMF
    image/x-emf

X_FONTDATA
    application/x-fontdata

X_FONT_TTF
    application/x-font-ttf

X_WMF
    image/x-wmf
