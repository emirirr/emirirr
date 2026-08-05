<!--
  Bu profil README'si bir "terminal" olarak tasarlanmıştır.
  Hareketin tamamı kendi kendine yeten SVG dosyalarının içindedir
  (GitHub, README'lerden <script> ve inline CSS'i temizler ama
  <img> ile gömülü SVG'lerin SMIL / CSS animasyonlarını oynatır).

  Parçalar:
    contrib-heatmap.svg  -> canlı katkı takvimi  (GitHub Actions ile her gün yenilenir)
    info-card.svg        -> neofetch tarzı kart   (statik; scripts/make_info_card.py)

  Yeniden üretmek için:
    pip install -r scripts/requirements.txt
    python scripts/fetch_contributions.py && python scripts/render_heatmap_svg.py
    python scripts/make_info_card.py
-->

<div align="center">

<h3><code>emir@github ~ $ ./contributions.sh</code></h3>

<img src="./contrib-heatmap.svg" width="820" alt="GitHub katkı grafiği" />

<br><br>

<h3><code>emir@github ~ $ whoami</code></h3>

<img src="./info-card.svg" width="600" alt="neofetch bilgi kartı" />

<br><br>

<h3><code>emir@github ~ $ ls ./links</code></h3>

<a href="https://emirtiryaki.com"><img src="https://img.shields.io/badge/portfolio-emirtiryaki.com-161b22?style=flat-square&logo=vercel&logoColor=39d353&labelColor=0d1117" alt="Portfolio" height="26" /></a>
<a href="https://emirtiryaki.com/projects"><img src="https://img.shields.io/badge/projeler-tümü-161b22?style=flat-square&logo=react&logoColor=39d353&labelColor=0d1117" alt="Projeler" height="26" /></a>
<a href="https://github.com/emirirr"><img src="https://img.shields.io/badge/github-emirirr-161b22?style=flat-square&logo=github&logoColor=39d353&labelColor=0d1117" alt="GitHub" height="26" /></a>
<a href="https://www.linkedin.com/in/emir-tiryaki/"><img src="https://img.shields.io/badge/linkedin-emir--tiryaki-161b22?style=flat-square&logo=linkedin&logoColor=39d353&labelColor=0d1117" alt="LinkedIn" height="26" /></a>
<a href="mailto:info@emirtiryaki.com"><img src="https://img.shields.io/badge/e--posta-info@emirtiryaki.com-161b22?style=flat-square&logo=gmail&logoColor=39d353&labelColor=0d1117" alt="E-posta" height="26" /></a>

<br><br>

<sub><code>emir@github ~ $</code> <em>katkı grafiği her gün ~06:17 UTC otomatik yenilenir · portre yok, neofetch + canlı heatmap</em></sub>

</div>
