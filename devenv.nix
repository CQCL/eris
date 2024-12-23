{ pkgs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [ pkgs.just ];

  enterShell = ''
    export PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"
  '';

  languages.python = {
    enable = true;
    uv = {
      enable = true;
      sync.enable = true;
      sync.allExtras = true;
    };
  };
}
