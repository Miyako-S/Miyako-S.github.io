<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:aws="http://webservices.amazon.com/AWSECommerceService/2005-03-23">
<!-- Copyright (c) 2004-2005 daisuke asano [spirits.of.zero@gmail.com]-->
<!-- Amazon to Javascript IMAGE(ECS4.0版 BEST SELLER) -->
<!-- 2005/04/16 修正 -->
<xsl:output method="html" encoding="UTF-8"/>

  <!-- ユーザー設定 -->
  <xsl:param name="setNoImageURL" select="'no image画像の設置URI'" />
  <!-- ユーザー設定ここまで -->

  <xsl:param name="AssociateTag" select="aws:ItemSearchResponse/aws:OperationRequest/aws:Arguments/aws:Argument[@Name = 'AssociateTag']/@Value"/>

  <xsl:template match="/">
    <xsl:text disable-output-escaping="yes">document.write('&lt;div id="aws-bestseller" style="width:175px; text-align:center;"&gt; &lt;div id="aws-link"&gt;')
    </xsl:text>

    <xsl:text disable-output-escaping="yes">document.write('</xsl:text>
    <xsl:element name="a"><xsl:attribute name="href">http://www.amazon.co.jp/exec/obidos/redirect?tag=<xsl:value-of select="$AssociateTag" />&amp;path=tg/browse/-/489986</xsl:attribute>Amazon.co.jp</xsl:element>
    <xsl:text disable-output-escaping="yes">&lt;/div&gt;')
    </xsl:text>

    <xsl:apply-templates select="aws:ItemSearchResponse/aws:Items/aws:Item">
      <xsl:sort select="aws:SalesRank" order="ascending"/>
    </xsl:apply-templates>
    
    <xsl:text disable-output-escaping="yes">document.write('&lt;/div&gt;')
    </xsl:text>
  </xsl:template>

  <xsl:template match="aws:Item" xmlns="http://www.w3.org/1999/xhtml">
    <xsl:param name="norma00" select="translate(aws:ItemAttributes/aws:Title, '&#34;', '”' )" />
    <xsl:param name="norma" select='translate($norma00, "&#39;", "’" )' />
    <xsl:choose>
      <xsl:when test="position() = 1">
	<xsl:text disable-output-escaping="yes">document.write('</xsl:text>
	<xsl:element name="a">
	  <xsl:attribute name="href">http://www.amazon.co.jp/exec/obidos/ASIN/<xsl:value-of select="aws:ASIN" />/<xsl:value-of select="$AssociateTag" />/ref=nosim</xsl:attribute>
	  <xsl:attribute name="target">_top</xsl:attribute>
	  <xsl:element name="img"><xsl:attribute name="alt"><xsl:value-of select="$norma" /></xsl:attribute><xsl:attribute name="title"><xsl:value-of select="$norma" /></xsl:attribute>
	    <xsl:choose>
	      <xsl:when test="aws:MediumImage">
		<xsl:attribute name="src"><xsl:value-of select="aws:MediumImage/aws:URL" /></xsl:attribute>
	      </xsl:when>
	      <xsl:otherwise>
		<xsl:attribute name="src"><xsl:value-of select="$setNoImageURL" />noimage_m.gif</xsl:attribute>
	      </xsl:otherwise>
	    </xsl:choose>
	  </xsl:element>
	</xsl:element>
	<xsl:text disable-output-escaping="yes">&lt;br /&gt;')
	</xsl:text>
      </xsl:when>

      <xsl:otherwise>
	<xsl:text disable-output-escaping="yes">document.write('</xsl:text>
	<xsl:element name="a">
	  <xsl:attribute name="href">http://www.amazon.co.jp/exec/obidos/ASIN/<xsl:value-of select="aws:ASIN" />/<xsl:value-of select="$AssociateTag" />/ref=nosim</xsl:attribute>
	  <xsl:attribute name="target">_top</xsl:attribute>
	  <xsl:element name="img"><xsl:attribute name="alt"><xsl:value-of select="$norma" /></xsl:attribute><xsl:attribute name="title"><xsl:value-of select="$norma" /></xsl:attribute>
	    <xsl:choose>
	      <xsl:when test="aws:SmallImage">
		<xsl:choose>
		  <xsl:when test="aws:SmallImage/aws:Width &gt; 53">
		    <xsl:attribute name="src"><xsl:value-of select="aws:SmallImage/aws:URL" /></xsl:attribute><xsl:attribute name="width">53</xsl:attribute>
		  </xsl:when>
		  <xsl:otherwise>
		    <xsl:attribute name="src"><xsl:value-of select="aws:SmallImage/aws:URL" /></xsl:attribute>
		  </xsl:otherwise>
		</xsl:choose>
	      </xsl:when>
	      <xsl:otherwise>
		<xsl:attribute name="src"><xsl:value-of select="$setNoImageURL" />noimage_s.gif</xsl:attribute>
	      </xsl:otherwise>
	    </xsl:choose>
	  </xsl:element>
	</xsl:element>
	<xsl:choose>
	  <xsl:when test="(position() = 4) or (position() = 7) or (position() = 10)">
	    <xsl:text disable-output-escaping="yes">&lt;br /&gt;')
	    </xsl:text>
	  </xsl:when>
	  <xsl:otherwise>
	    <xsl:text disable-output-escaping="yes">')
	    </xsl:text>
	  </xsl:otherwise>
	</xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
