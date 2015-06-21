<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" indent="yes" />
<!-- Copyright (c) 2004-2005 daisuke asano [spirits.of.zero@gmail.com]-->
<!-- Amazon to Javascript TEXT -->
<!-- 2005/04/04 修正 -->

  <xsl:param name="n" select="ProductInfo/Request/Args/Arg[@name = 'n']/@value" />
  <xsl:param name="dev-t" select="ProductInfo/Request/Args/Arg[@name = 'dev-t']/@value" />
  <xsl:param name="t" select="ProductInfo/Request/Args/Arg[@name = 't']/@value" />

  <xsl:template match="/">
    <xsl:text disable-output-escaping="yes">document.write('&lt;div id="amazontojs"&gt;')
    </xsl:text>

    <xsl:apply-templates select="ProductInfo/Details">
      <xsl:sort select="SalesRank" order="ascending" />
    </xsl:apply-templates>

    <xsl:text disable-output-escaping="yes">document.write('&lt;/div"&gt;')
    </xsl:text>
  </xsl:template>

  <!-- 商品検索結果の生成 -->
  <xsl:template match="Details">
    <xsl:choose>
      <xsl:when test="($n &gt;= 1) and ($n &lt;= 10)">
	<xsl:call-template name="Items">
	  <xsl:with-param name="nn" select="$n" />
	</xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
	<xsl:call-template name="Items">
	  <xsl:with-param name="nn" select="10" />
	</xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="Items">
    <xsl:param name="nn" />
    <xsl:if test="position() &lt;= $nn">
      
    <xsl:text disable-output-escaping="yes">var str= "</xsl:text>
<xsl:value-of select="translate(ProductName, '&#34;','”' )" />
<xsl:text disable-output-escaping="yes">"; str.replace("&#39;","’");</xsl:text>

    <xsl:text disable-output-escaping="yes">document.write('</xsl:text>
    <xsl:element name="a"><xsl:attribute name="href">http://www.amazon.co.jp/exec/obidos/ASIN/<xsl:value-of select="Asin" />/<xsl:value-of select="$t" />/ref=nosim</xsl:attribute>' + str + '</xsl:element>
    <xsl:text disable-output-escaping="yes">&lt;br /&gt;')
    </xsl:text>

    <xsl:text disable-output-escaping="yes">document.write('</xsl:text>
    <xsl:choose>
      <xsl:when test="Catalog = 'Music'">
	<xsl:value-of select="Artists/Artist" />
      </xsl:when>
      <xsl:when test="Catalog = 'Book'">
	<xsl:value-of select="Authors/Author" />
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="Manufacturer" />
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text disable-output-escaping="yes">')
    </xsl:text>
     
    <xsl:text disable-output-escaping="yes">document.write('</xsl:text>
    <xsl:choose>
      <xsl:when test="OurPrice"> (<xsl:value-of select="translate(OurPrice, '￥ ','')" />円)</xsl:when>
      <xsl:otherwise> (-- 円)</xsl:otherwise>
    </xsl:choose>
    <xsl:text disable-output-escaping="yes">&lt;br /&gt;')
    </xsl:text>

  </xsl:if>
  </xsl:template>
</xsl:stylesheet>
