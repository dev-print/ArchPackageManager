pkgname=archpackagemanager
pkgver=1.0.0
pkgrel=1
pkgdesc="A simple Arch Linux package manager with a GUI"
arch=('any')
url="https://github.com/yourusername/ArchPackageManager"
license=('MIT')
depends=('python' 'python-pyqt5')
source=("https://github.com/yourusername/ArchPackageManager/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/ArchPackageManager-$pkgver"
    install -Dm755 src/main.py "$pkgdir/usr/bin/archpackagemanager"
    install -Dm644 README.md "$pkgdir/usr/share/doc/archpackagemanager/README.md"
    install -Dm644 PRIVACY_POLICY.md "$pkgdir/usr/share/doc/archpackagemanager/PRIVACY_POLICY.md"
}