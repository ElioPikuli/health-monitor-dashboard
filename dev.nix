{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.sqlite
    pkgs.docker
    pkgs.docker-compose
  ];

  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
    ];
    
    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Create a virtual environment and install dependencies
        install = "python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Ensure venv is activated (though usually handled by shell hooks or manual activation)
      };
    };
  };
}
