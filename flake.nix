{
  description = "WplaceM";
  inputs = {
    nixpkgs.url = "git+file:///home/toni/Documents/source/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
      buildInputs = [
        (pkgs.python3Full.withPackages (python-pkgs: [
          python-pkgs.tkinter
          python-pkgs.opencv4
          python-pkgs.pyautogui
          #python-pkgs.mss
          python-pkgs.pillow
        ]))
        pkgs.tk
        pkgs.wmctrl
      ];
    in {
      devShells.default = pkgs.mkShell {
        inherit buildInputs;
      };
    });
}
