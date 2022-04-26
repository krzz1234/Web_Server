<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<style>
.error {color: #FF0000;}
</style>
<body>
  <h2>Investment Portfolio</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th style="text-align:left">Stock</th>
      <th style="text-align:left">Quantity</th>
      <th style="text-align:left">Price</th>
      <th style="text-align:left">Gain/Loss</th>
    </tr>
    <xsl:for-each select="catalog/stock">
    <tr>
      <td><xsl:value-of select="@symbol"/></td>
      <td><xsl:value-of select="quantity"/></td>
      <td><xsl:value-of select="price"/></td>
      <td><xsl:value-of select="gainNloss"/></td>
    </tr>
    </xsl:for-each>
  </table>
  <br />

  <form method="post" action="">
    Stock Symobl: <input type="text" name="stock"></input><br></br>
    Quantity:     <input type="text" name="quantity"></input><br></br>
    Price:        <input type="text" name="price"></input><br></br>
  <br />
    <input type="reset" id="btn_res" name="btn_res" value="Reset" />
    <input type="submit" id="btn_sub" name="btn_sub" value="Update" />
  </form>
</body>
</html>
</xsl:template>
</xsl:stylesheet>

