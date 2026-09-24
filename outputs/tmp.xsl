<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <head><meta charset="UTF-8"/></head>
  <body>
  <xsl:if test="dict/known">
    <h2>Tone words (known before #1)</h2>
    <xsl:for-each select="dict/known/hanzi">
      <h3><xsl:value-of select="@char"/></h3>
      <xsl:for-each select="word">
        <xsl:value-of select="m"/> - <xsl:value-of select="p"/> - <xsl:value-of select="d"/><br/>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="dict/hanzi">
    <h2>Char #<xsl:value-of select="@id + 1"/>: <xsl:value-of select="@char"/></h2>
    <xsl:for-each select="word">
       <xsl:value-of select="m"/> - <xsl:value-of select="p"/> - <xsl:value-of select="d"/><br/>
    </xsl:for-each>
    <h3>Examples:</h3>
      <ul><xsl:for-each select="sentences/sent">
         <li><xsl:value-of select="current()"/></li>
         </xsl:for-each>
      </ul>
  </xsl:for-each>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
