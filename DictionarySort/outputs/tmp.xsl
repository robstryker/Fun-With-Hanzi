<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Stuff</h2>
  <xsl:for-each select="dict/hanzi">
    <h2>Char #<xsl:value-of select="@id"/>: <xsl:value-of select="@char"/></h2>
    [<a><xsl:attribute name="href">http://www.nciku.com/search/all/<xsl:value-of select="@char"/></xsl:attribute>nciku</a>] [<a><xsl:attribute name="href">http://www.mandarintools.com/cgi-bin/wordlook.pl?searchtype=pinyin&amp;where=whole&amp;word=<xsl:value-of select="@char"/></xsl:attribute>mandarintools</a>] 

<br/>
    <xsl:for-each select="word">
       [<a>
           <xsl:attribute name="href">
             http://www.nciku.com/search/all/<xsl:value-of select="m"/>
           </xsl:attribute>a</a>] 
       <xsl:value-of select="m"/> - <xsl:value-of select="p"/> - <xsl:value-of select="d"/><br/>
    </xsl:for-each>
    <h3>Examples:</h3>
      <ul><xsl:for-each select="sentences/sent">
         <li>[<a>
           <xsl:attribute name="href">
             http://www.nciku.com/search/all/examples/<xsl:value-of select="current()"/>
           </xsl:attribute>T</a>] 
           [<a>
              <xsl:attribute name="href">
                http://translate.google.com/#zh-CN|en|<xsl:value-of select="current()"/>
              </xsl:attribute>GT</a>]
           <xsl:value-of select="current()"/></li>
         </xsl:for-each>
      </ul>
  </xsl:for-each>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
