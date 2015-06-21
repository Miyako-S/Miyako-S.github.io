<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" indent="yes" />
<!-- Copyright (c) 2004-2005 daisuke asano [spirits.of.zero@gmail.com]-->
<!-- Amazon to Javascript IMAGE -->
<!-- 2005/04/04 修正 -->

  <!-- ユーザー設定 -->
  <xsl:param name="setNoImageURL" select="'no image画像の設置URI'" />
  <xsl:param name="setImageSize" select="1 or 2" />
  <!-- ユーザー設定ここまで -->

  <xsl:param name="n" select="ProductInfo/Request/Args/Arg[@name = 'n']/@value" />
  <xsl:param name="dev-t" select="ProductInfo/Request/Args/Arg[@name = 'dev-t']/@value" />
  <xsl:param name="t" select="ProductInfo/Request/Args/Arg[@name = 't']/@value" />

  <xsl:template match="/">
    <xsl:text disable-output-escaping="yes">document.write('&lt;div id="amazontojs"&gt;')
    </xsl:text>

    <xsl:apply-templates select="ProductInfo/Details">
      <xsl:sort select="SalesRank" order="ascending" />
    </xsl:apply-templates>

    <xsl:text disable-output-escaping="yes">document.write('&lt;/div&gt;')
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
    <xsl:element name="a">
      <xsl:attribute name="href"><xsl:value-of select="@url" /></xsl:attribute>
	  <xsl:attribute name="target">_blank</xsl:attribute>
      <xsl:element name="img">
	<xsl:attribute name="src">
	  <xsl:choose>
	    <xsl:when test="$setImageSize = 1"><xsl:value-of select="ImageUrlSmall" /></xsl:when>
	    <xsl:when test="$setImageSize = 2"><xsl:value-of select="ImageUrlMedium" /></xsl:when>
	  </xsl:choose>
	</xsl:attribute>
	<xsl:attribute name="border">0</xsl:attribute>
	<xsl:attribute name="onload">if (this.width==\'1\' &amp;&amp; this.src.match(/\.01\./)) { this.src=\'<xsl:value-of select="$setNoImageURL" />noimage_s.gif\'; } else if (this.width==\'1\') { this.src=this.src.replace(\'.09.\',\'.01.\'); }</xsl:attribute>
      </xsl:element>
	  <xsl:text disable-output-escaping="yes">&lt;br /&gt;→Amazonへ</xsl:text>
    </xsl:element>
    <xsl:text disable-output-escaping="yes">')
    </xsl:text>

    
  </xsl:if>
  </xsl:template>
</xsl:stylesheet>
