pkgname=archpackagemanager
pkgver=1.3
pkgrel=1
pkgdesc="A simple Arch Linux package manager with a GUI"
arch=('any')
url="https://github.com/dev-print/ArchPackageManager"
license=('MIT')
depends=('python' 'python-pyqt5')
source=("https://github.com/dev-print/ArchPackageManager/archive/refs/tags/1.3.tar.gz"
        "icons/archpackagemanager.png")
sha256sums=('SKIP' 'SKIP')

package() {
    cd "$srcdir/ArchPackageManager-$pkgver"
    install -Dm755 src/main.py "$pkgdir/usr/bin/archpackagemanager"
    install -Dm644 README.md "$pkgdir/usr/share/doc/archpackagemanager/README.md"
    install -Dm644 PRIVACY_POLICY.md "$pkgdir/usr/share/doc/archpackagemanager/PRIVACY_POLICY.md"
    install -Dm644 archpackagemanager.desktop "$pkgdir/usr/share/applications/archpackagemanager.desktop"
    install -Dm644 icon/archpackagemanager.png "$pkgdir/usr/share/pixmaps/archpackagemanager.png"
}
